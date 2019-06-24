import configparser
import sys


def read_config_file(config_file_path):
    """Load configuration file and creates a dict with the necessary attributes

    :param config_file_path: The path file to be read
    :return: A dict with the attributes read from the file
    """
    config = configparser.ConfigParser()
    config.read(config_file_path)

    config_dict = {
        'orion_host': config.get('orion', 'host'),
        'orion_port': config.getint('orion', 'port'),
        'sth_host': config.get('sthcomet', 'host'),
        'sth_port': config.getint('sthcomet', 'port'),
        'cygnus_host': config.get('cygnus', 'host'),
        'cygnus_port': config.getint('cygnus', 'port'),
        'device_type': config.get('device', 'device_type'),
        'device_id': config.get('device', 'device_id'),
        'device_schema_path': config.get('device', 'device_schema_path'),
    }

    return config_dict


if __name__ == "__main__":
    print(read_config_file('config.ini'))
