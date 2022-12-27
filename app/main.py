import configparser
import argparse
import asyncio
import logging
import sys
from hashlib import sha512
from zc.lockfile import LockFile, LockError
from typing import Dict, Any

from utils.db_handler import DBHandler
import actions
import scrapers


def has_updated(new_state: str, old_state: str) -> bool:
    if old_state is None:
        return True
    new_hash = sha512(new_state.encode('utf-8')).hexdigest()
    old_hash = sha512(old_state.encode('utf-8')).hexdigest()
    return new_hash != old_hash


async def process_source(db: DBHandler, source: Dict[str, Any]) -> None:
    source_id = int(source['id'])
    source_name = source.get('name', source_id)
    if 'params' not in source:
        logging.error('Missing source params for %s.', source_name)
        return
    if 'source' not in source['params']:
        logging.error('Missing source location for %s.', source_name)
        return
    source_type = source['params'].get('type', 'html')
    source_scraper = source['params'].get('scraper', 'dummy')
    source_actions = source['params'].get('actions', [])
    if not source_actions:
        logging.error('No actions specified for %s.', source_name)
        return
    if source_type not in scrapers.SUPPORTED_TYPES:
        logging.error('Source %s type is not supported.', source_name)
        return
    if source_scraper not in scrapers.SCRAPERS_REGISTRY:
        logging.error('Source %s scraper is not supported.', source_name)
        return
    scraper = scrapers.SCRAPERS_REGISTRY[source_scraper](source_name, source['params'])
    new_state = await scraper.scrape()
    old_state = await db.latest_state(source_id)
    if has_updated(new_state, old_state):
        await db.upsert_state(source_id, new_state)
        for source_action in source_actions:
            if source_action not in actions.ACTIONS_REGISTRY:
                logging.error('Unknown action %s for source %s.', source_action, source_name)
            action = actions.ACTIONS_REGISTRY[source_action]()
            action.action('{} updated: {}'.format(source_name, new_state))


async def main(loop: asyncio.AbstractEventLoop) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(levelname)s - %(message)s',
    )

    try:
        lock = LockFile('.lock')
    except LockError:
        logging.error('Cannot obtain lock — is the app already running?')
        sys.exit(0)

    db_host = config.get('db', 'host')
    db_user = config.get('db', 'user')
    db_password = config.get('db', 'password')
    db_name = config.get('db', 'name')
    db = DBHandler(
        host=db_host,
        user=db_user,
        password=db_password,
        name=db_name,
        loop=loop,
    )
    await db.setup()

    sources = await db.list_sources()
    tasks = [
        asyncio.create_task(
            process_source(db, source)
        ) for source in sources
    ]
    await asyncio.gather(*tasks)

    await db.destroy()
    lock.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
