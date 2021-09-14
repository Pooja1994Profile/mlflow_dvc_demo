# All the test cases function should start with test_function_name
import json
import logging
import os
import joblib
import pytest
from prediction_service.prediction import form_response, api_response
import prediction_service

input_data = {
    "incorrect_range":
        {"gre_score": 7897897,
         "toefl_score": 555,
         "university_rating": 99,
         "sop": 99,
         "lor": 12,
         "cgpa": 789,
         "research": 0
         },

    "correct_range":
        {"gre_score": 330,
         "toefl_score": 119,
         "university_rating": 4,
         "sop": 4,
         "lor": 3,
         "cgpa": 7,
         "research": 1
         },

    "incorrect_col":
        {"Gre score": 340,
         "toefl_score": 119,
         "university_rating": 4,
         "sop": 4,
         "lor": 3,
         "cgpa": 6,
         "research": 1
         }
}

TARGET_range = {
    "min": 0.0,
    "max": 100.0
}


def test_form_response_correct_range(data=input_data['correct_range']):
    res = form_response(data)
    print(res)
    assert TARGET_range['min'] <= res <= TARGET_range['max']


def test_api_response_correct_range(data=input_data['correct_range']):
    res = api_response(data)
    print(res)
    assert TARGET_range['min'] <= res['response'] <= TARGET_range['max']


def test_form_response_incorrect_range(data=input_data['incorrect_range']):
    with pytest.raises(prediction_service.prediction.NotInRange):
        res = form_response(data)


def test_api_response_incorrect_range(data=input_data['incorrect_range']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInRange().message


def test_form_response_incorrect_col(data=input_data['incorrect_col']):
    with pytest.raises(prediction_service.prediction.NotInCols):
        res = form_response(data)


def test_api_response_incorrect_col(data=input_data['incorrect_col']):
    res = api_response(data)
    assert res['response'] == prediction_service.prediction.NotInCols().message
