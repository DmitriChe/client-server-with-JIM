# pip install pyyaml
# python server.py
# python server.py -c config yml
# python server.py -a 127.0.0.1 -p 7777
# python server.py -a localhost -p 7777
# Пересылка: str -> bytes -> compress -> send -> recv -> decompress -> bytes -> str

import yaml
import json
import socket
import logging
from argparse import ArgumentParser
from actions import resolve
from protocol import validate_request, make_response
from handlers import handle_default_request



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
    'buffersize': 1024  # размер буфера для приема сообщений клиента
}

# Если в командной строке указали аргумент с config файлом, то берем данные оттуда и перезаписываем ими словарь config
if args.config:
    with open(args.config) as file:
        file_config = yaml.load(file, Loader=yaml.Loader)
        config.update(file_config)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('main.log'),
        logging.StreamHandler(),
    ]
)

# Вычленяем данные для подключения из config
host, port = config.get('host'), config.get('port')

# Если данные о подключени переданы в командной строке, то берем их оттуда
if args.addr:
    host = args.addr
if args.port:
    port = args.port

# Обработчик ошибки KeyboardInterrupt при нажатии Ctrl+C, Ctrl+D, Ctrl+BackSpace
try:
    # Создаем объект sock - абстакцию над программно-аппаратным сокетом системы.
    sock = socket.socket()  # socket() это конструктор сокета. В него можно передать протокол и дескриптор
    # bind - привязываем сокет к IP-адресу и порту машины
    sock.bind((host, port))
    # Связали. Теперь можно прослушивать порт на предмет запросов Клиента
    # listen - просигнализировать о готовности принимать соедение (аргументом явл число возможных подключений)
    sock.listen(5)  # Может обрабатыват 5 одновременных подключений
    # И отчитываемся, что
    logging.info(f'Server started with { host }:{ port }')

    # Создаем бесконечный цикл ожидаиня сервером - прослушку
    while True:
        client, address = sock.accept()
        logging.info(f'Client was detected { address[0] }:{ address[1]}')
        # Пока реализуем простой эхо-сервер: сервер плучает от клиента сообщение и отсылает его в ответ
        b_request = client.recv(config.get('buffersize'))  # Получаем сообщеие клиента
        b_response = handle_default_request(b_request)
        client.send(b_response)
        client.close()

except KeyboardInterrupt:
    print('Server shotdown.')  # Вывод сообщения, что клиет завершил свое выполнение


# Список функций для сокетов
# Общие:
# socket - конструктор объекта сокета (с методами сединения). Сокет - программный интерфейс, позволяющий отправлть данные по сети. Пара буферых файлов для хранения передаваемых данных, ip, port, программный интерфейс, который все это обслуживает, драйвера сетевой.... OSI
# send - передать данные
# recv - получить данные
# close - закрыть соединение
# Серверные:
# bind - привязать сокет к IP-адресу и порту машины
# listen - просигнализировать о готовности принимать соедение (аргументом явл число возможных подключений)
# accept - подтверждение принятия запроса на устанговку соединения
# Клиентские:
# connect - установить соединение