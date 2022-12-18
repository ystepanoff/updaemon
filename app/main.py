import configparser
import argparse
import asyncio
import logging
import sys
from zc.lockfile import LockFile, LockError
from typing import Dict, Any

from utils.db_handler import DBHandler


async def process_source(db: DBHandler, source: Dict[str, Any]) -> None:
    print(source)


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
