# Запуск теста из консоли: pytest server (точки - ОК, F - fail)
import pytest  # для описания атомарных фикстур
from datetime import datetime
from protocol import make_response


# описываем фикстуры
@pytest.fixture
def expected_action():
    return 'test'

@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_data():
    return 'Some data'

@pytest.fixture
def expected_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': datetime.now().timestamp(),
        'data': expected_data,
    }

#
# # Константа
# ACTION = 'test'
#
# CODE = '200'
#
# DATA = 'Some data'
#
# REQUEST = {
#     'action': ACTION,
#     'time': datetime.now().timestamp(),
#     'data': DATA,
# }
#
# # Описываем ожидаемый ответ в виде объекта
# RESPONSE = {
#     'action': ACTION,
#     'time': datetime.now().timestamp(),
#     'code': CODE,
#     'data': DATA,
# }
#
# # Описываем тесты с префиксом test_ т.е. что будет ли наш запрос REQUEST соответсвовать нашему ожидаемому ответу RESPONSE
# def test_action_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('action') == ACTION
#
# def test_code_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('code') == 200
#
# def test_data_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('data') == DATA


def test_action_make_response(expected_request, expected_action, expected_code, expected_data):
    actual_response = make_response(
        expected_request, expected_code, expected_data
    )
    assert actual_response.get('action') == expected_action

def test_code_make_response(expected_request, expected_code, expected_data):
    actual_response = make_response(
        expected_request, expected_code, expected_data
    )
    assert actual_response.get('code') == expected_code

def test_data_make_response(expected_request, expected_code, expected_data):
    actual_response = make_response(
        expected_request, expected_code, expected_data
    )
    assert actual_response.get('data') == expected_data
