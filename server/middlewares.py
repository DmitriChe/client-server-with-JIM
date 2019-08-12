# Пред- и постобработчики в виде декораторов
# Реализуем декомпрессию и компрессию данных, чтобы передавать меньше, а получать больше)
import zlib
from functools import wraps  # импортируем декоратор wrap


# Декомпрессия & компрессия
def compression_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        bytes_request = zlib.decompress(request)
        bytes_response = func(bytes_request, *args, **kwargs)
        return zlib.compress(bytes_response)
    return wrapper

# Сквозное шифрование
def encryption_middleware(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        # decrypt request
        bytes_response = func(request, *args, **kwargs)
        # encrypt response
        return bytes_response
    return wrapper