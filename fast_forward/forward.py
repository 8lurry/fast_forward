# -*- coding: UTF-8 -*-
# Copyright 2023 8lurry <sharifmehedi24@outlook.com>
# License: GNU Affero General Public License v3 (see file COPYING for details)

import atexit
import logging
import signal
import socket
import sys
import threading

format = '%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO, format=format)


def handle(buffer, direction, src_address, src_port, dst_address, dst_port):
    '''
    intercept the data flows between local port and the target port
    '''
    if direction:
        logging.debug(f"{src_address, src_port} -> {dst_address, dst_port} {len(buffer)} bytes")
    else:
        logging.debug(f"{src_address, src_port} <- {dst_address, dst_port} {len(buffer)} bytes")
    return buffer


def transfer(src, dst, direction, closables=None):
    @atexit.register
    def closer():
        src.close()
        dst.close()

    if closables is None:
        closables = []
    src_address, src_port = src.getsockname()
    dst_address, dst_port = dst.getsockname()
    while True:
        try:
            buffer = src.recv(4096)
            if len(buffer) > 0:
                dst.send(handle(buffer, direction, src_address, src_port, dst_address, dst_port))
        except Exception as e:
            logging.error(repr(e))
            break
    if 1 in closables:
        logging.info(f"Closing socket {src_address, src_port}")
        src.close()
    if 2 in closables:
        logging.info(f"Closing socket {dst_address, dst_port}")
        dst.close()


def get_socket() -> socket.socket:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return sock


def remote(remote_host: str, remote_port: int, local_host: str = "127.0.0.1", local_port: int = 22):
    remote_sock = get_socket()
    remote_sock.connect((remote_host, remote_port))
    logging.info(f"Connected to {remote_host, remote_port} to get content")
    ssh_sock = get_socket()
    ssh_sock.connect((local_host, local_port))
    logging.info(f"Connected to {local_host, local_port} sshd")

    @atexit.register
    def closer():
        remote_sock.close()
        ssh_sock.close()

    def handler(*args):
        sys.exit()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    try:
        incoming = threading.Thread(target=transfer, args=(remote_sock, ssh_sock, True, [1, 2]))
        outgoing = threading.Thread(target=transfer, args=(ssh_sock, remote_sock, False, [1, 2]))
        incoming.start()
        outgoing.start()
    except Exception as e:
        logging.error(repr(e))


def local(accept_port: int, send_port: int, hostname: str = "0.0.0.0"):
    reverse_socket = get_socket()
    reverse_socket.bind((hostname, send_port))
    reverse_socket.listen()
    logging.info(f"Server started for reverse connection {hostname, send_port}")
    server_socket = get_socket()
    server_socket.bind((hostname, accept_port))
    server_socket.listen(0x40)
    logging.info(f"Server started {hostname, accept_port}")

    @atexit.register
    def closer():
        logging.info(f"Closing socket {hostname, send_port}")
        reverse_socket.close()
        logging.info(f"Closing socket {hostname, accept_port}")
        server_socket.close()

    def handler(*args):
        sys.exit()

    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    while True:
        src_socket, src_address = reverse_socket.accept()
        logging.info(f"Reverse connection established with {src_address}")
        while True:
            client_socket, client_address = server_socket.accept()
            logging.info(f"Connection established with {client_address}")
            try:
                logging.info(f"[OK] {client_address} -> {src_address}")
                outgoing = threading.Thread(target=transfer, args=(src_socket, client_socket, False, [2]))
                incoming = threading.Thread(target=transfer, args=(client_socket, src_socket, True, [1]))
                outgoing.start()
                incoming.start()
            except Exception as e:
                logging.error(repr(e))

        src_socket.close()
