from .controllers import get_echo


# Собственно это "таламус" - здесь происходит переключение информации на релевантную ей функцию
# т.е. на ту функцию, которая годится для обработки именно этой иноформации. Хэндлер - обрботчки зарпоса пользователя
# И вот этот список ассоциаций и есть ядра таламуса.
actionnames = [
    {'action': 'echo', 'controller': get_echo}  # Создаем связь между именем действия (echo) и самим действием (функция get_echo)
]