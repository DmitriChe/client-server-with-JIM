# Утилитарный модуль для утилитарных, вспомогательных функци, позволяющих производить валидацию
# и регламентировать взаимодействие клиента и сервера
from datetime import datetime


# Валидация объекта запроса клиента на предмет наличия необходимых полей action и time
def validate_request(request):
    if 'action' in request and 'time' in request:
        return True
    return False

# Функция генерирующая стандартный ответ сервера
# code - код ответа сервера (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)
def make_response(request, code, data=None):
    return {
        'action': request.get('action'),
        'time': datetime.now().timestamp(),
        'code': code,
        'data': data,
    }
