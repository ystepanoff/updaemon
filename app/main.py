import configparser
import argparse
import asyncio

from utils.db_handler import DBHandler


async def main(loop: asyncio.AbstractEventLoop) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

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

    await db.test_mysql()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop))
    finally:
        loop.close()