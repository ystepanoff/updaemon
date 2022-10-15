import configparser
import argparse

CONFIG = configparser.ConfigParser()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True)
    args = parser.parse_args()
    CONFIG.read(args.config)
    print(CONFIG.get('db', 'host'))