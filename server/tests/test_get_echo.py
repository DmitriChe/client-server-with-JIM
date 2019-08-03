import pytest
from datetime import datetime
from server.echo.controllers import get_echo


@pytest.fixture
def expected_action():
    return 'test'

@pytest.fixture
def expected_code():
    return 200

@pytest.fixture
def expected_data():
    return 'Some data'

# Комбинированная фикстура на основании предыдущих
@pytest.fixture
def initial_request(expected_action, expected_data):
    return {
        'action': expected_action,
        'time': datetime.now().timestamp(),
        'data': expected_data,
    }


# Передаем фикстуры в функции
def test_action_get_echo(initial_request, expected_action):
    actual_response = get_echo(initial_request)
    assert actual_response.get('action') == expected_action


def test_code_get_echo(initial_request, expected_code):
    actual_response = get_echo(initial_request)
    assert actual_response.get('code') == expected_code


def test_data_get_echo(initial_request, expected_data):
    actual_response = get_echo(initial_request)
    assert actual_response.get('data') == expected_data


# def test_time_get_echo(initial_request, expected_action, expected_code, expected_data):
#     actual_response = get_echo(initial_request)
#     assert actual_response.get('time') == expected_action
#
#
#
# def test_code_make_response(initial_request, expected_code, expected_data):
#     actual_response = make_response(
#         initial_request, expected_code, expected_data
#     )
#     assert actual_response.get('code') == expected_code
#
# def test_data_make_response(initial_request, expected_code, expected_data):
#     actual_response = make_response(
#         initial_request, expected_code, expected_data
#     )
#     assert actual_response.get('data') == expected_data
