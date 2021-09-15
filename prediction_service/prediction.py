import yaml
import os
import json
import joblib
import numpy as np
from sklearn.preprocessing import StandardScaler
from logger_error import log_error


params_path = "params.yaml"
schema_path = os.path.join("prediction_service", "schema_in.json")


class NotInRange(Exception):
    """
    Custom exception for feature are not in given range in schema_in
    """
    def __init__(self, message="Values entered are not in expected range"):
        self.message = message
        super().__init__(self.message)


class NotInCols(Exception):
    """
        Custom exception for feature are same as expected model
    """
    def __init__(self, message="Not in cols"):
        self.message = message
        super().__init__(self.message)


def read_params(config_path=params_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def predict(data):
    """
    This function will take data from web app and will do model predict.
    :param data: data from web app
    :return: prediction value
    """
    config = read_params(params_path)
    model_dir_path = config["webapp_model_dir"]
    model = joblib.load(model_dir_path)

    scaler = StandardScaler()
    data = scaler.fit_transform(data)

    prediction = float(model.predict(data).tolist()[0])*100
    try:
        if 0 < prediction <= 100:
            return prediction
        else:
            raise NotInRange
    except NotInRange:
        log_obj = log_error()
        log_obj.dvc_logger(str(NotInRange))
        return "Unexpected result"


def get_schema(schema_path=schema_path):
    with open(schema_path) as json_file:
        schema = json.load(json_file)
    return schema


def validate_input(dict_request):
    """
    This will take json format date and do model prediction.
    :param dict_request: Json data
    :return: prediction
    """
    def _validate_cols(col):
        schema = get_schema()
        actual_cols = schema.keys()
        if col not in actual_cols:
            log_obj = log_error()
            log_obj.dvc_logger(str(NotInCols))
            raise NotInCols

    def _validate_values(col, val):
        schema = get_schema()

        if not (schema[col]["min"] <= float(dict_request[col]) <= schema[col]["max"]):
            log_obj = log_error()
            log_obj.dvc_logger(str(NotInRange))
            raise NotInRange

    for col, val in dict_request.items():
        _validate_cols(col)
        _validate_values(col, val)

    return True


def form_response(dict_request):
    if validate_input(dict_request):
        data = dict_request.values()
        data = [list(map(float, data))]
        response = predict(data)
        return response


def api_response(dict_request):
    try:
        if validate_input(dict_request):
            data = np.array([list(dict_request.values())])
            response = predict(data)
            response = {"response": response}
            return response
    except Exception as e:
        response = {"response": str(e)}
        return response
