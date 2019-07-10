import json
from pathlib import Path
import os.path

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

def create_config_file():
        path = Path('data/config.json')
        if not os.path.isfile(path):
            with open(path,'w+') as config_file:
                json_config = {"cores_to_use": 1,
                        "number_of_trees": 5,
                        "factor": 2,
                        "dataset": "sample_dataset.csv"}
                json.dump(json_config, config_file, indent=4)

        else:
                print("Config file alredy exists")