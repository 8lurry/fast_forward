# -*- coding: UTF-8 -*-
# Copyright 2023 8lurry <sharifmehedi24@outlook.com>
# License: GNU Affero General Public License v3 (see file COPYING for details)

import argparse
from fast_forward.forward import local


def main(parser: argparse.ArgumentParser = None):
    if parser is None:
        parser = argparse.ArgumentParser()
    parser.add_argument("--hostname", type=str, help="the host to listen", default="0.0.0.0")
    parser.add_argument("--client-port", type=int, help="the port to bind", required=True)
    parser.add_argument("--reverse-port", type=int, help="the port to bind for reverse connection", required=True)
    args = parser.parse_args()
    local(args.client_port, args.reverse_port, args.hostname)


if __name__ == "__main__":
    main()
