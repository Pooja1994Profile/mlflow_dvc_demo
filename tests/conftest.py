# Whatever you extract here can be direct used into the test_config.py file
import pytest
import yaml
import os
import json


@pytest.fixture
def config(config_path='params.yaml'):
    """
    Read params.yaml file and store into the config variable
    :param config_path: params.yaml file
    :return: config
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


@pytest.fixture
def schema_in(schema_path='schema_in.json'):
    """
    Read schema_in.json file that contain dataset features with min and max value
    :param schema_path: schema_in.json file
    :return: schema
    """
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema
