import socket 
import threading

from server_utils.config.db_config import *
from server_utils.ClientService import *
from classes import *


# GLOBAL CONSTANTS
HOST = '127.0.0.1'
PORT = 8000
ADDR = (HOST, PORT)

# GLOBAL VARIABLES
chats = []
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv_sock.bind(ADDR)


def serve_conn(sock : socket.socket, addr : tuple) -> None :

    # Create database connection for each session.
    conn = DBConnector()

    client_service = ClientService(conn)
    client_service.serve_client(sock)

    print(f'[SERVED] Client at {addr[0]}:{addr[1]} served.')


def accept_conns(serv_sock : socket.socket, n_conns : int) -> None :
    serv_sock.listen(n_conns)
    print('[START] Server started.')

    while True :
        # Serve every new connection in separate thread.
        sock, addr = serv_sock.accept()
        print(f'[ACCEPT] Connection from {addr[0]}:{addr[1]} accepted.')
        thread = threading.Thread(target=serve_conn, args=(sock, addr))
        thread.run()


if __name__ == '__main__' :
    print('[START] Server starting...')
    accept_conns(serv_sock, 8)