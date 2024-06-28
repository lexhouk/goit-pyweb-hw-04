from http.server import BaseHTTPRequestHandler, HTTPServer
from mimetypes import guess_type
from pathlib import Path

ROOT = Path('front-init')


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        code = 200

        path = self.path
        path = ROOT.joinpath('index.html' if path == '/' else path[1:])

        if not path.exists():
            code = 404
            path = ROOT.joinpath('error.html')

        self.send_response(code)
        self.send_header('Content-Type', guess_type(path)[0] or 'text/plain')

        self.end_headers()

        with open(path, 'rb') as file:
            self.wfile.write(file.read())


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
