import pandas as pd
import numpy as np
import os
import argparse
from get_data import read_params


def pre_processing(config_path):
    config = read_params(config_path)
    raw_data_path = config['load_data']['raw_dataset_csv']
    process_dataset_csv = config['preprocessing_data']['process_dataset_csv']
    drop_col = config['preprocessing_data']['drop_col']

    df = pd.read_csv(raw_data_path, sep=',')
    df = df.drop(columns=[drop_col])

    df['University_Rating'] = df['University_Rating'].fillna(df['University_Rating'].mode()[0])
    df['TOEFL_Score'] = df['TOEFL_Score'].fillna(df['TOEFL_Score'].mean())
    df['GRE_Score'] = df['GRE_Score'].fillna(df['GRE_Score'].mean())

    df.to_csv(process_dataset_csv, sep=',', encoding='utf-8')


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    pre_processing(config_path=parsed_args.config)