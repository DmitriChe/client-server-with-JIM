# Модуль, который по имени приложения в списке  модуля settings.py позволяет
# динамически выполнять импорт всего содержимого проекта (нужный модуль, actions, actionnames)
from functools import reduce  # для реализации функциональных парадигм (map, filter, reduce) в решении вместо объектных для лаконичности
from settings import INSTALLED_APPS
# from .settings import INSTALLED_APPS

# Создаем перечень всех имеющихся приложений (модулей, аппликейшенов) - как раз value содержит все элементы,
# как результат итераций по коллекции INSTALLED_APPS
def get_server_actions():
    modules = reduce(
        lambda value, item: value + [__import__(f'{item}.actions')],
        INSTALLED_APPS,
        [],  # Это значение по умолчанию для value, если оно не было определено
    )
    # Теперь формируем последовательность всех имеющихся подмодулей actions
    actions = reduce(
        lambda value, item: value + [getattr(item, 'actions', [])],  # [] - значение по умолчанию для item
        modules,
        [],
    )
#     Формирование списков всех возможных actionnames
    return reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        actions,  # ранее сформированный список всех имеющихся подмодулей actions
        []  # значение по умоланию для value
    )


def resolve(acton_name, actions=None):
    action_list = actions or get_server_actions()  # т.е. если actions окажется пустым, то берем все actions с сервера
    # связываем имя экшена с его контроллером (имя действия с самим действием, с функцией) в словаре, как ключ:значение
    action_mapping = {
        action.get('action'): action.get('controller')
        for action in action_list
    }
    return action_mapping.get(acton_name)  # возвращаем контроллер по имени action, т.е. по названию действия
