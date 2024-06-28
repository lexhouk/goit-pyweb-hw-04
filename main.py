from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type
from pathlib import Path
from urllib.parse import unquote_plus, urlparse
from json import dump, load
from json.decoder import JSONDecodeError
from datetime import datetime

ROOT = Path('front-init')


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
            items = self.rfile.read(int(size)).decode().split('&')
            items = [item.split('=') for item in items]
            items = {key: unquote_plus(value) for key, value in items if value}

            if items:
                if (path := ROOT.joinpath('storage/data.json')).exists():
                    with open(path, encoding='utf-8') as file:
                        try:
                            data = load(file)
                        except JSONDecodeError:
                            ...

                if 'data' not in locals() or type(data) is not dict:
                    data = {}

                # 2022-10-29 20:20:58.020261
                data[datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')] = items

                with open(path, 'w', encoding='utf-8') as file:
                    dump(data, file, ensure_ascii=False, indent=2)

        self.send_response(302)
        self.send_header('Location', '/message.html')
        self.end_headers()


def main() -> None:
    ADDRESS = ('localhost', 3000)

    print(f'Navigate to http://{ADDRESS[0]}:{ADDRESS[1]} to visit your '
          'website.')

    try:
        server = HTTPServer(ADDRESS, Handler)
        server.serve_forever()
    except KeyboardInterrupt:
        print('Server is stoped.')
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
