# # Описываем тесты с префиксом test_ , чтобы модуль pytest их опознал и САМ запустил как тесты
# pip install pytest
# Запуск теста из консоли: pytest server (точки - ОК, F - fail)
# pip install pytest-cov
# Узнать, сколько кода покрыто тестами
# В консоли: pytest --cov server
# Узнать, сколько кода НЕ покрыто тестами в процентрах, с указанием диапазона строк кода
# В консоли: pytest --cov-report term-missing --cov server
import pytest  # для описания атомарных фикстур
from datetime import datetime
# Импортируем ТЕСТИРУЕМУЮ функцию. Функция make_response формирует объект ответа сервера. Вот это мы и тестируем.
from protocol import make_response

# ФИКСТУРЫ как "динамические", многофункциональные константы
# описываем фикстуры, предварительно импортировав модуль pytest
# описывая фикстуры мы формируем аргументы, которые затем можем передавать в такие же фикстуры или тестовые функции
# если внутри приложения не найдется аргумента, сответствующего фикстуре, которую мы описали, то в этом случае
# pytest вывалит ошибку. Ссылаясь на то, что мы пытаемся использовать фикстуру, которую не создали
# Фиекстуры это функции и поэтому в них можно описывать дополнитлеьную логику.
#  Т.е. фикстура - это константа с возможностями функции!! В ней содержится не только значение, но может быть прописана
# еще и дополнительная логика. Например подключение к базе данных, откуда берется значение константы и др. Или здесь же
# значения можно получить вычисленимем - т.е. это гибкий аппарат формирования проверяемых данных
# Декоратор фикстура формирует значение в памяти на основе заключенной в него функции.
# Т.е. прямо в процессе компиляции текста программы, дойдя до фикстуры происходит отработка заключенной функции
# и ее трезультат помещается в память в переменную с именем функции.
# Далее это значение используется в программе
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

#
# # Константы
# ACTION = 'test'
# CODE = '200'
# DATA = 'Some data'
#
#  #Создаем запрос, как в клиенте
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
# # Описываем тесты с префиксом test_ , чтобы модуль pytest их опознал и САМ запустил как тесты
# # здесь тестируем, будет ли наш запрос REQUEST соответсвовать нашему ожидаемому ответу RESPONSE
# # Проверяем, такой ли 'action', как мы указали в образце, выдает сервер в ответ на наш запрос
# def test_action_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('action') == ACTION
#
# # Проверяем, такой ли 'code', как мы указали в образце, выдает сервер в ответ на наш запрос
# def test_code_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('code') == 200
#
# def test_data_make_response():
#     actual_response = make_response(REQUEST, CODE, DATA)
#     assert actual_response.get('data') == DATA

# Передаем фикстуры в функции
def test_action_make_response(initial_request, expected_action, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
    )
    assert actual_response.get('action') == expected_action

def test_code_make_response(initial_request, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
    )
    assert actual_response.get('code') == expected_code

def test_data_make_response(initial_request, expected_code, expected_data):
    actual_response = make_response(
        initial_request, expected_code, expected_data
    )
    assert actual_response.get('data') == expected_data
