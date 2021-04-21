import yaml


def import_config_file(path):
    """
    Imports the contents of an entire yaml file into a dictionary
    for future use

    Args:
        path (string): path to a yaml file

    Returns:
        (dict): dictionary of yaml key-value pairs
    """
    with open(path) as config_file:
        config_data = yaml.load(config_file, Loader=yaml.FullLoader)
    return config_data


def get_docker_port(base_path='./', path='docker-compose.yml'):
    """
    Import exposed port number for gRPC server to be run on from
    'docker-compose.yml'

    Args:
        base_path (string): Base path string
        path (string): path to docker-compose.yml

    Returns:
        (str): port number as a string
    """
    config = import_config_file(base_path + path)
    return config["services"]["ubuntu-tensorflow-cardetection"]["expose"][0]


def parse_yaml_string_to_dict(conf_str):
    """
    Receive config as yaml formatted string and parse it into dictionary

    Args:
        conf_str (str): yaml formatted string

    Returns:
        (dict): config dictionary to be passed to the EventDetector class
    """
    conf_dict = yaml.load(conf_str, Loader=yaml.Loader)
    return conf_dict
