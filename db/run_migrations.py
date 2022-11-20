import argparse
import configparser
import pymysql.cursors
import os
import re


def find_new_migrations(existing_migrations, dir):
    migrations = []
    for file in os.listdir(dir):
        match = re.match('(\d{3})-(.*).sql$', file)
        if match:
            id = int(match[1])
            description = match[2]
            if (id, description) not in existing_migrations:
                migrations.append((id, description, file))
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

    migrations = find_new_migrations([], args.dir)
