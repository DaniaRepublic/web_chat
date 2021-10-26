import socket 
import threading

from server_utils.config.db_config import *
from server_utils.ClientService import *


# GLOBAL CONSTANTS
HOST = '127.0.0.1'
PORT = 8080
ADDR = (HOST, PORT)

# SERVER SOCKET
try:
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind(ADDR)
except Exception as e:
    serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serv_sock.bind((HOST, 0))
    ADDR = serv_sock.getsockname()

# DB CONNECTION
conn_pool = DBConnector()


class ClientThread(threading.Thread):
    def __init__(self, csock, caddr, conn):
        threading.Thread.__init__(self)
        self.csock = csock
        self.caddr = caddr
        self.conn = conn

    def run(self):
        client_service = ClientService(self.conn, ADDR)
        client_service.serve_client(self.csock)
        print(f'[SERVED] Client at {self.caddr[0]}:{self.caddr[1]} served.')


def accept_conns(serv_sock : socket.socket, n_conns : int) -> None :
    serv_sock.listen(n_conns)
    print(f'[START] Server started at { ADDR[0] }:{ ADDR[1] }/')

    while True :
        print('[WAITING] Waiting for connection.')
        sock, addr = serv_sock.accept()
        print(f'[ACCEPT] Connection from {addr[0]}:{addr[1]} accepted.')
        conn = conn_pool.connect()
        # Serve every new connection in separate thread.
        newthread = ClientThread(sock, addr, conn)
        newthread.start()


if __name__ == '__main__' :
    accept_conns(serv_sock, 8)