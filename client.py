import zlib
import json
import yaml  # pip install pyyaml
import socket
import threading
from datetime import datetime
from argparse import ArgumentParser

WRITE_MODE = 'write'  # константа режима работы клиента
READ_MODE = 'read'  # константа режима работы клиента


def read(sock, buffersize):
    while True:
        response = sock.recv(buffersize)  # получаем ответ
        bytes_response = zlib.decompress(response)  # декомпрессия ответа сервера
        print(bytes_response.decode())  # декодируем, превращая в обычную стороку


# Делим клиент на два подклиента: один для отправки сообщений (write), другой для получения (чтения)
def make_request(action, data):
    # Формируем и отдаем объект пользовательского запроса
    return {
        'action': action,
        'time': datetime.now().timestamp(),  # текущая дата в виде timestamp
        'data': data,
    }


# На сервере и клиенте host и port должны совпадать - а как это обеспечить в независимых приложениях?
# Через файл config.yml
# А если файла не будет? А если его переименют?
# А для этого предусмотрим возможнось задавать его имя из командной строки при запуске приложения,
# а оттуда будем парсить настройки с помощью ArgumentParser


# Создание парсера командной строки для анализа запроса: python client.py -c config.yml
parser = ArgumentParser()

parser.add_argument(
    '-c', '--config', type=str,  # Описываем параметры (-c - сокращенное имя для командной строки или --config - полное имя, которое испльзуется далее в args.config) для командной строки и допустимый тип данных - str
    required=False,  # Задаем, что этот аргумент является необязательным
    help='Sets config file path'  # Сообщение при вызове помощи
)
parser.add_argument(
    '-a', '--addr', type=str,  # Описываем параметры (-c - сокращенное имя для командной строки или --config - полное имя, которое испльзуется далее в args.config) для командной строки и допустимый тип данных - str
    required=False,  # Задаем, что этот аргумент является необязательным
    help='Sets ip-адрес сервера'  # Сообщение при вызове помощи
)
parser.add_argument(
    '-p', '--port', type=int,  # Описываем параметры (-c - сокращенное имя для командной строки или --config - полное имя, которое испльзуется далее в args.config) для командной строки и допустимый тип данных - str
    required=False,  # Задаем, что этот аргумент является необязательным
    help='Sets tcp-порт сервера'  # Сообщение при вызове помощи
)

# Считываем аргументы из командной строки
args = parser.parse_args()

# Создадим словарь со знаениями по умолчанию - default configuration
# Т.е. если в командрой стоке не указан конфигурационный файл, в качестве параметра,
# а лишь python client.py, то берем данные отсюда:
config = {
    'host': 'localhost', # здесь используем локальный хост
    'port': 7777,  # номер порта на сетевой карте.
    'buffersize': 1024,  # размер буфера для приема сообщений клиента
}

# Если в командной строке указали аргумент с config файлом, то берем данные оттуда и перезаписываем ими словарь config
if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)


# Вычленяем данные для подключения из config
host, port = config.get('host'), config.get('port')

# Если данные о подключени переданы в командной строке, то берем их оттуда
if args.addr:
    host = args.addr
if args.port:
    port = args.port

# Обработчик ошибки KeyboardInterrupt при нажатии Ctrl+C, Ctrl+D, Ctrl+BackSpace
try:
    # Создадим клентскую адресную пару - хост и порт
    # Создаем объект socket - абстракцию над аппаратно-программной системой сетевой карты, драйверов, буферных файлов, софта, ip, port
    sock = socket.socket()
    # Подключаемся
    sock.connect((host, port))
    print(f'Client was started with { host }:{ port }\n')

    # Запускаем поток с процессом чтения сообщений сервера
    read_thread = threading.Thread(
        target=read, args=(sock, config.get('buffersize'))
    )
    read_thread.start()  # запускаем поток

    # запускаем клиент в бесконечном цикле
    while True:
        # Данные: ввод и вывод
        action = input('Enter action: ')
        data = input('Enter data: ')
        request = make_request(action, data)
        # Получаем строку из запроса в формате json (из словаря с данными запроса request)
        str_request = json.dumps(request)
        # Кодирование и компрессия введенных пользователем данных
        bytes_request = zlib.compress(str_request.encode())
        # Отправляем сжатые данные на сокет сервера для передачи по сети
        sock.send(bytes_request)
        print(f'Client send data { data }\n')
        # КОНЕЦ отправки

except KeyboardInterrupt:
    print('Client shutdown.')  # Вывод сообщения, что клиет завершил свое выполнение

# Список функций для сокетов
# Общие:
# socket - конструктор объекта сокета (с методами сединения). Сокет - программный интерфейс, позволяющий отправлть
# данные по сети. Пара буферых файлов для хранения передаваемых данных, ip, port, программный интерфейс,
# который все это обслуживает, драйвера сетевой.... OSI
# send - передать данные
# recv - получить данные
# close - закрыть соединение
# Серверные:
# bind - привязать сокет к IP-адресу и порту машины
# listen - просигнализировать о готовности принимать соедение (аргументом явл число возможных подключений)
# accept - подтверждение принятия запроса на устанговку соединения
# Клиентские:
# connect - установить соединение
