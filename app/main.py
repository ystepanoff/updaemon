from typing import Dict, Any
import configparser
import argparse
import asyncio
import logging
import traceback
import sys
from hashlib import sha512
from zc.lockfile import LockFile, LockError

from utils.db_handler import DBParams, DBHandler
import actions
import scrapers


def has_updated(new_state: str, old_state: str) -> bool:
    if old_state is None:
        return True
    new_hash = sha512(new_state.encode('utf-8')).hexdigest()
    old_hash = sha512(old_state.encode('utf-8')).hexdigest()
    return new_hash != old_hash


async def process_source(db_handler: DBHandler, source: Dict[str, Any]) -> None:
    source_id = int(source['id'])
    old_state = await db_handler.latest_state(source_id)
    scraper_data = await db_handler.find_scraper(source_id)
    if scraper_data is not None:
        try:
            scraper = getattr(scrapers, scraper_data['base_class'])(
                remote=source.get('remote'),
                params=scraper_data.get('params', {})
            )
            new_state = await scraper.scrape()
            if has_updated(new_state, old_state['data']):
                actions_data = await db_handler.list_actions(source_id)
                for action_data in actions_data:
                    action = getattr(actions, action_data['base_class'])(**action_data['params'])
                    await action.action(
                        meta='Updated: {}'.format(source['remote']),
                        message='Updated: {}'.format(source['remote']),
                    )
                await db_handler.upsert_state(source_id, new_state)
        except AttributeError:
            traceback.print_exc()
            logging.error('Wrong scraper %s for source %s.', scraper_data['base_class'], source_id)
    else:
        logging.error('Could not find any scrapers for source %s.', source_id)


async def main() -> None:
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

    db_handler = DBHandler(
        params=DBParams(
            host=config.get('db', 'host'),
            user=config.get('db', 'user'),
            password=config.get('db', 'password'),
            name=config.get('db', 'name'),
        ),
    )
    await db_handler.setup()

    sources = await db_handler.list_sources()
    tasks = [
        asyncio.create_task(
            process_source(db_handler, source)
        ) for source in sources
    ]
    await asyncio.gather(*tasks)

    await db_handler.destroy()
    lock.close()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
