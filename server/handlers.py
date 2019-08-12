# промежуточное ПО в виде декораторов: пре и постобработка данных
# обработчик запроса пользователя
import json
import logging
from actions import resolve
from protocol import validate_request, make_response
# импорт рукодельного декоратора-предобработчика (компрессор-декомпрессор)
from middlewares import compression_middleware, encryption_middleware


# Сверва декомпрессия, затем дешифрование, затем хендлер, затем шифрование ответа сервера, затем компрессия
@compression_middleware
@encryption_middleware
def handle_default_request(bytes_request):
    # Декодируем запрос пользователя и переформатируем его в формат json
    request = json.loads(bytes_request.decode())
    # Проводим валидацию запроса на предмет наличия требуемых полей
    # Если все в порядке, то запускаем обработчик запроса - handler
    if validate_request(request):
        action_name = request.get('action')  # берем из запроса имя требуемого действия
        controller = resolve(
            action_name)  # и по этому имени получаем контроллер (т.е. функцию, принимающую объект запроса)
        if controller:  # если контроллер существует, то
            try:
                logging.info(f'Client send valid request {request}')
                # И генерируем ответ сервера из запроса, кода ответа сервера и данных
                response = controller(
                    request)  # запускаем контроллер (т.е. функцию, действие, принимающую объект запроса)
            except Exception as err:
                logging.critical(f'Internal server error: {err}')
                response = make_response(request, 500, data='Internal server error')
        else:
            logging.error(f'Controller with action name {action_name} does not exists')
            response = make_response(request, 404, 'Action not found')
    # Иначе:
    else:
        logging.error(f'Client send invalid request {request}')
        response = make_response(request, 404, 'Wrong request')

    # Форматируем в json, кодируем и отсылаем клиенту обратно его сообщение: "эхо"
    str_response = json.dumps(response)
    return str_response.encode()