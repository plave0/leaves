import json
from pathlib import Path

def change_config(setting, value):
    
    config = load_config()

    config[setting] = value
    
    path = Path('data/config.json').absolute()
    with open(path, 'w') as config_file:
        json.dump(config, config_file,indent=4)

def load_config():
    path = Path('data/config.json')
    with open(path) as config_file:
        config = json.load(config_file)
    return config