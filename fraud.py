import io
import logging
from json import dumps
from time import sleep

from flask import Flask
from requests import request
from multiprocessing import Process
from contextlib import contextmanager, redirect_stdout

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


class Server:
    def __init__(self, host, port, data):
        self.__host__ = host
        self.__port__ = port
        self.__data__ = data

    @contextmanager
    def run(self):
        p = Process(target=self.server)
        p.start()
        sleep(1)
        yield
        p.kill()

    def server(self):
        _ = io.StringIO()
        with redirect_stdout(_):
            app = Flask(__name__)

            @app.route('/')
            def index():
                return dumps(self.__data__)

            app.run(self.__host__, self.__port__)


if __name__ == '__main__':
    data = [
        {"name": "Brut", "found": "glass balls"},
        {"name": "Pouhru", "found": "a clay man, oak leaves"},
        {"name": "Dihsu", "found": "chestnuts, a crust of bread"},
        {"name": "Hary", "found": "a necklace of shells, a picture book"},
        {"name": "Kitt", "found": "branches in the closet"},
        {"name": "Irtox", "found": "stones under the bed"},
        {"name": "Hax", "found": "a pot of potsherds, coins in pockets"}
    ]

    server = Server('127.0.0.1', 8080, data)
    with server.run():
        while (row := input('Введите "stop" для завершения работы сервера: ')) != 'stop':
            ...
