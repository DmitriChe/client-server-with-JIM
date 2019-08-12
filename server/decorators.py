import logging
from functools import wraps


logger = logging.getLogger('decorators')


# Создаем декоратот по журналированию
def logged(func):
    def wrapper(request, *args, **kwargs):
        logger.debug(f'{func.__name__}: {request}')
        return func(request, *args, **kwargs)
    return wrapper
