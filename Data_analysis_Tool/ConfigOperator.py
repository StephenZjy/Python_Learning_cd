import yaml


def read_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


def filter_config(config_data, keywords):
    return {key: value for key, value in config_data.items() if keywords in key}
