from typing import List
import os
import re
import argparse
import configparser
import pymysql.cursors


def find_new_migrations(existing_migrations: List[int], migrations_dir: str) -> List[tuple]:
    migrations = []
    print(existing_migrations)
    for migration_file in sorted(os.listdir(migrations_dir)):
        match = re.match(r'(\d{3})-(.*).sql$', migration_file)
        if match:
            migration_id = int(match[1])
            migration_name = match[2]
            if migration_id not in existing_migrations:
                migrations.append((migration_id, migration_name, migration_file))
    if migrations:
        print('Found new migrations:')
        for _, _, migration_file in migrations:
            print(migration_file)
    return migrations


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    parser.add_argument('--dir', type=str, required=True)
    args = parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)

    db_name = config.get('db', 'name')

    with pymysql.connect(
            host=config.get('db', 'host'),
            user=config.get('db', 'user'),
            password=config.get('db', 'password'),
            client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS,
    ) as connection:
        existing_migrations = []
        try:
            connection.select_db(db_name)
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM migrations")
                existing_migrations = [id for (id,) in cursor.fetchall()]
                print("Existing migrations:", existing_migrations)
        except pymysql.err.OperationalError as exception:
            error_id, *_ = exception.args
            if error_id == pymysql.constants.ER.BAD_DB_ERROR:
                with connection.cursor() as cursor:
                    cursor.execute(f"CREATE DATABASE {db_name}")
                connection.select_db(db_name)
        except pymysql.err.ProgrammingError as exception:
            error_id, *_ = exception.args
            if error_id == pymysql.constants.ER.BAD_TABLE_ERROR:
                # there is no migrations table, so start from the very first migration
                pass
        with connection.cursor() as cursor:
            new_migrations = find_new_migrations(existing_migrations, args.dir)
            for migration_id, name, migration_file in new_migrations:
                with open(os.path.join(args.dir, migration_file), 'rt', encoding='utf-8') as file:
                    sql = file.read()
                    try:
                        cursor.execute(sql)
                        cursor.execute("""
                            INSERT INTO migrations (id, name) VALUES (%s, %s)
                        """, (migration_id, name))
                        print(f'Applied migration: {migration_file}')
                    except pymysql.err.Error as exception:
                        print(f'{migration_file}: {exception}')
        connection.commit()


if __name__ == '__main__':
    main()
