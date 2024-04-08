import io
import logging
from json import dumps
from time import sleep

from flask import Flask
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
        {"being": "elf Humboldt", "job": "get a glass casket"},
        {"being": "blue kobold", "job": "quid pro quo"},
        {"being": "fairy of the forest", "job": "magic scent"},
        {"being": "dwarf", "job": "pot of gold"},
        {"being": "troll from the hills", "job": "baton"},
        {"being": "elf Ariel", "job": "ringing of the higher spheres"},
        {"being": "hobbit Baggins", "job": "good day"}
    ]

    server = Server('127.0.0.1', 8080, data)
    with server.run():
        while (row := input('Р’РІРµРґРёС‚Рµ "stop" РґР»СЏ Р·Р°РІРµСЂС€РµРЅРёСЏ СЂР°Р±РѕС‚С‹ СЃРµСЂРІРµСЂР°: ')) != 'stop':
            ...