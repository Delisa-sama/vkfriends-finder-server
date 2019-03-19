import configparser
from os.path import exists

config_filename = 'config.ini'
config = configparser.ConfigParser()
config['DEFAULT'] = {
    'port': 8080,
    'vk_api_version': '5.92',
    'vk_api_app_id': '6798117',
    'vk_api_lang': 'ru',
    'vk_api_timeout': 10,
    'static_path': './static'
}
if not exists(config_filename):
    with open(config_filename, 'w') as configfile:
        config.write(configfile)
else:
    config.read(config_filename)

config = config['DEFAULT']
