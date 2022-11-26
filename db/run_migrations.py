import argparse
import configparser
import pymysql.cursors
import os
import re
from typing import List


def find_new_migrations(existing_migrations: List[int], dir: str) -> List[tuple]:
    migrations = []
    for file in os.listdir(dir):
        match = re.match('(\d{3})-(.*).sql$', file)
        if match:
            id = int(match[1])
            name = match[2]
            if id not in existing_migrations:
                migrations.append((id, name, file))
    if migrations:
        print('Found new migrations:')
        for _, _, file in migrations:
            print(file)
    return migrations


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--dir', type=str, required=True)
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    db_host = config.get('db', 'host')
    db_user = config.get('db', 'user')
    db_password = config.get('db', 'password')
    db_name = config.get('db', 'name')

    with pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
    ) as connection:
        existing_migrations = []
        try:
            connection.select_db(db_name)
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM migrations")
                existing_migrations = [id for (id,) in cursor.fetchall()]
                print("Existing migrations:", existing_migrations)
        except pymysql.err.OperationalError as e:
            error_id, _ = e.args
            if error_id == pymysql.constants.ER.BAD_DB_ERROR:
                with connection.cursor() as cursor:
                    cursor.execute("CREATE DATABASE {}".format(db_name))
                connection.select_db(db_name)
        except pymysql.err.ProgrammingError as e:
            error_id, _ = e.args
            if error_id == pymysql.constants.ER.BAD_TABLE_ERROR:
                # there is no migrations table, so start from the very first migration
                pass
        with connection.cursor() as cursor:
            new_migrations = find_new_migrations(existing_migrations, args.dir)
            for id, name, file in new_migrations:
                with open(os.path.join(args.dir, file), 'rt') as migration_file:
                    sql = migration_file.read()
                    try:
                        cursor.execute(sql)
                        cursor.execute("INSERT INTO migrations (id, name) VALUES (%s, %s)", (id, name))
                        print('Applied migration: {}'.format(file))
                    except pymysql.err.Error as e:
                        print('{}: {}'.format(file, str(e)))
        connection.commit()
