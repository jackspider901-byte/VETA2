"""Serve the editable prototype locally using Python's standard library.
Usage: python3 serve.py [--port 8000]
The server binds only to this computer. Press Ctrl+C to stop.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import argparse

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port',type=int,default=8000)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error('Port must be between 1 and 65535.')
    root = Path(__file__).resolve().parent
    try:
        server = ThreadingHTTPServer(('127.0.0.1',args.port),partial(SimpleHTTPRequestHandler,directory=str(root)))
    except OSError as error:
        parser.exit(1,f'Could not start the server: {error}\nTry a different --port.\n')
    print(f'Prototype: http://127.0.0.1:{args.port}/index.html')
    print(f'Screen gallery: http://127.0.0.1:{args.port}/preview/index.html')
    print('Press Ctrl+C to stop.')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nServer stopped.')
    finally:
        server.server_close()

if __name__ == '__main__':
    main()
