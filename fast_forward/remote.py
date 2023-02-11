# -*- coding: UTF-8 -*-
# Copyright 2023 8lurry <sharifmehedi24@outlook.com>
# License: GNU Affero General Public License v3 (see file COPYING for details)


import argparse
from fast_forward.forward import remote


def main(parser: argparse.ArgumentParser = None):
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument("--remote-host", type=str, help="the target host to connect", required=True)
    parser.add_argument("--remote-port", type=int, help="the target port to connect", required=True)
    parser.add_argument("--local-host", type=str, help="the local host to connect", default="127.0.0.1")
    parser.add_argument("--local-port", type=int, help="the local port to connect", default=22)
    args = parser.parse_args()
    remote(args.remote_host, args.remote_port, args.local_host, args.local_port)


if __name__ == "__main__":
    main()

