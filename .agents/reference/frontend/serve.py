"""Máy chủ trình diễn cục bộ; không dùng để triển khai sản xuất."""
import argparse
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from pathlib import Path
from functools import partial

class DemoHandler(SimpleHTTPRequestHandler):
    backend = 'http://127.0.0.1:8765'
    def do_GET(self):
        if self.path.startswith('/api/v1/'):
            try:
                headers={k:self.headers[k] for k in ('Authorization','Accept') if k in self.headers}
                with urlopen(Request(self.backend + self.path,headers=headers), timeout=3) as response:
                    self.send_response(response.status)
                    self.send_header('Content-Type','application/json');
                    if response.headers.get('X-Request-ID'):self.send_header('X-Request-ID',response.headers['X-Request-ID'])
                    self.end_headers();self.wfile.write(response.read())
            except HTTPError as exc:
                self.send_response(exc.code);self.send_header('Content-Type','application/json');
                if exc.headers.get('X-Request-ID'):self.send_header('X-Request-ID',exc.headers['X-Request-ID'])
                self.end_headers();self.wfile.write(exc.read())
            except URLError:
                self.send_error(503,'Máy chủ không khả dụng')
            return
        if self.path.split('?')[0] == '/items':self.path='/index.html'
        super().do_GET()

if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8766);p.add_argument('--backend-port',type=int,default=8765);args=p.parse_args()
    DemoHandler.backend=f'http://127.0.0.1:{args.backend_port}'
    with ThreadingHTTPServer(('127.0.0.1',args.port),partial(DemoHandler,directory=str(Path(__file__).resolve().parent))) as server:server.serve_forever()
