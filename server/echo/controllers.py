from protocol import make_response
# Импортируем декоратор logged из файла decorators
from decorators import logged


# И декорируем им имеющуюся функцию get_echo
@logged
def get_echo(request):
    data = request.get('data')
    return make_response(request, 200, data)
