import pandas as pd
import numpy as np
import os
import argparse
# noinspection PyUnresolvedReferences
from get_data import read_params
from logger_error import log_error


def pre_processing(config_path):
    """
    This function will read dataframe from data/raw and replace null value with mean/mode/median.
    Also, remove irrelevant cols. Save df to data/preprocessing
    :param config_path: dataframe path
    :return: None
    """
    try:
        config = read_params(config_path)
        raw_data_path = config['load_data']['raw_dataset_csv']
        process_dataset_csv = config['preprocessing_data']['process_dataset_csv']
        # drop_col = config['preprocessing_data']['drop_col']

        df = pd.read_csv(raw_data_path, sep=',')

        df['University_Rating'] = df['University_Rating'].fillna(df['University_Rating'].mode()[0])
        df['TOEFL_Score'] = df['TOEFL_Score'].fillna(df['TOEFL_Score'].mean())
        df['GRE_Score'] = df['GRE_Score'].fillna(df['GRE_Score'].mean())

        df = df.drop('Serial_No.', axis='columns')

        df.to_csv(process_dataset_csv, sep=',', index=False, encoding='utf-8')
    except Exception as e:
        print(e)
        log_obj = log_error()
        log_obj.dvc_logger(str(e))
        raise e


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    pre_processing(config_path=parsed_args.config)