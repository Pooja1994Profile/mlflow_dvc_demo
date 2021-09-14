import os
import pandas as pd
import warnings
import sys
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ElasticNet
from urllib.parse import urlparse
# noinspection PyUnresolvedReferences
from get_data import read_params
import argparse
import joblib
import json


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def train_and_evaluate(config_path):
    config = read_params(config_path)
    test_data_path = config['split_data']['test_path']
    train_data_path = config['split_data']['train_path']
    random_state = config['base']['random_state']
    model_dir = config['model_dir']

    alpha = config['estimators']['ElasticNet']['params']['alpha']
    l1_ratio = config['estimators']['ElasticNet']['params']['l1_ratio']

    target = [config["base"]["target_col"]]

    train = pd.read_csv(train_data_path, sep=",")
    test = pd.read_csv(test_data_path, sep=",")

    train_y = train[target]
    test_y = test[target]

    train_x = train.drop(target, axis=1)
    test_x = test.drop(target, axis=1)

    scaler = StandardScaler()
    s_train_x = scaler.fit_transform(train_x)
    s_test_x = scaler.fit_transform(test_x)
    print(s_train_x)
    print(s_test_x)

    lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=random_state)
    lr.fit(s_train_x, train_y)

    predicted_qualities = lr.predict(s_test_x)
    # print(lr.predict([[321.0, 111.0, 3.0, 3.5, 4.0, 8.83, 1]]))
    (rmse, mae, r2) = eval_metrics(test_y, predicted_qualities)

    scores_file = config['reports']['scores']
    params_file = config['reports']['params']

    with open(scores_file, 'w') as f:
        scores = {
            "rmse": rmse,
            'mae': mae,
            'r2': r2
        }
        json.dump(scores, f, indent=4)

    with open(params_file, 'w') as f:
        params = {
            "rmse": rmse,
            'mae': mae,
            'r2': r2
        }
        json.dump(params, f, indent=4)

    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, 'model.joblib')

    joblib.dump(lr, model_path)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    train_and_evaluate(config_path=parsed_args.config)
