import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split
# noinspection PyUnresolvedReferences
from get_data import read_params
from logger_error import log_error


def split_and_saved_data(config_path):
    """
    This function read dataset from data/preprocessing and split df into train & test.
    Save both df's to data/processed
    :param config_path:
    :return: None
    """
    try:
        config = read_params(config_path)
        test_data_path = config['split_data']['test_path']
        train_data_path = config['split_data']['train_path']
        process_data_path = config['preprocessing_data']['process_dataset_csv']
        split_ratio = config['split_data']['test_size']
        random_state = config['base']['random_state']

        df = pd.read_csv(process_data_path, sep=',')

        train, test = train_test_split(df, test_size=split_ratio, random_state=random_state)

        train.to_csv(train_data_path, sep=',', index=False, encoding='utf-8')
        test.to_csv(test_data_path, sep=',', index=False, encoding='utf-8')
    except Exception as e:
        print(e)
        log_obj = log_error()
        log_obj.dvc_logger(str(e))
        raise e


if __name__=='__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    split_and_saved_data(config_path=parsed_args.config)