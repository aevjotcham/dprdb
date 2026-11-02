"""Build and preview: python3 -m server localhost:6700."""

import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

from build import build


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("address", nargs="?", default="localhost:6700")
    args = parser.parse_args()
    host, separator, port = args.address.rpartition(":")
    if not separator or not host or not port.isdecimal() or not 1 <= int(port) <= 65535:
        parser.error("use HOST:PORT, for example localhost:6700")
    directory = build()
    handler = partial(SimpleHTTPRequestHandler, directory=str(directory))
    with ThreadingHTTPServer((host, int(port)), handler) as server:
        print(f"Preview: http://{args.address} (Ctrl+C to stop)", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
