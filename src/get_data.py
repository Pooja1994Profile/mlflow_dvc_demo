import os
import yaml
import pandas as pd
import argparse
from logger_error import log_error


def read_params(config_path):
    """
        Read yaml file and store into the config variable
        :param config_path: expecting yaml file
        :return: config
    """
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def get_data(config_path):
    """
    This function will read dataset, create dataframe and return dataframe
    :param config_path: path of the dataset
    :return: dataframe of the dataset
    """
    try:
        config = read_params(config_path)
        data_path = config['data_source']['s3_source']
        df = pd.read_csv(data_path, sep=',', encoding='utf-8')
        return df
    except Exception as e:
        print(e)
        log_obj = log_error()
        log_obj.dvc_logger(str(e))
        raise e


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    data = get_data(config_path=parsed_args.config)
