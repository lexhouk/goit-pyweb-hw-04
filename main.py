from abc import ABC
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from json import dump, load
from json.decoder import JSONDecodeError
from logging import INFO, basicConfig, info
from mimetypes import guess_type
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket
from threading import Thread
from urllib.parse import unquote_plus, urlparse

ROOT = Path('www')
ADDRESS = '127.0.0.1', 5000


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        code = 200

        path = urlparse(self.path).path
        path = ROOT.joinpath('index.html' if path == '/' else path[1:])

        if not path.exists():
            code = 404
            path = ROOT.joinpath('error.html')

        self.send_response(code)
        self.send_header('Content-Type', guess_type(path)[0] or 'text/plain')
        self.end_headers()

        with open(path, 'rb') as file:
            self.wfile.write(file.read())

    def do_POST(self) -> None:
        if size := self.headers.get('Content-Length'):
            client = SocketServer.init()
            client.sendto(self.rfile.read(int(size)), ADDRESS)
            client.close()

        self.send_response(302)
        self.send_header('Location', '/message.html')
        self.end_headers()


class Server(ABC, Thread):
    def __init__(self, name: str, host: str, port: int) -> None:
        super().__init__(name=f'{name} server')
        self._address = host, port
        self.start()


class WebServer(Server):
    def run(self) -> None:
        server = HTTPServer(self._address, Handler)

        info(f'Navigate to http://{self._address[0]}:{self._address[1]} to '
             'visit your website.')

        try:
            server.serve_forever()
        except KeyboardInterrupt:
            info('Stopped.')
        finally:
            server.server_close()


class SocketServer(Server):
    @staticmethod
    def init() -> socket:
        return socket(AF_INET, SOCK_DGRAM)

    def run(self) -> None:
        server = self.init()
        server.bind(self._address)

        try:
            while True:
                content, _ = server.recvfrom(1_024)

                items = content.decode().split('&')
                items = [map(unquote_plus, item.split('=')) for item in items]
                items = {key: value for key, value in items if value}

                if items:
                    if (path := ROOT.joinpath('storage/data.json')).exists():
                        with open(path, encoding='utf-8') as file:
                            try:
                                data = load(file)
                            except JSONDecodeError:
                                ...

                    if 'data' not in locals() or type(data) is not dict:
                        data = {}

                    # E.g.: 2022-10-29 20:20:58.020261
                    key = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

                    data[key] = items

                    with open(path, 'w', encoding='utf-8') as file:
                        dump(data, file, ensure_ascii=False, indent=2)
        except KeyboardInterrupt:
            info('Stopped.')
        finally:
            server.close()


def main() -> None:
    basicConfig(level=INFO, format='%(threadName)s: %(message)s')

    WebServer('HTTP', '0.0.0.0', 3000)
    SocketServer('Socket', *ADDRESS)


if __name__ == '__main__':
    main()
