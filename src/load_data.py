# noinspection PyUnresolvedReferences
from get_data import read_params, get_data
import argparse
from logger_error import log_error


def load_and_save(config_path):
    """
    This function will load dataframe, update columns name and store dataframe to data/raw
    :param config_path: dataframe path
    :return: None
    """
    try:
        config = read_params(config_path)
        df = get_data(config_path)
        new_cols = [col.replace(" ", "_") for col in df.columns]
        raw_data_path = config['load_data']['raw_dataset_csv']
        df.to_csv(raw_data_path, sep=',', index=False, header=new_cols)
    except Exception as e:
        print(e)
        log_obj = log_error()
        log_obj.dvc_logger(str(e))
        raise e


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", default='params.yaml')
    parsed_args = args.parse_args()
    load_and_save(config_path=parsed_args.config)