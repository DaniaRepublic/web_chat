from .ChatService import ChatService
from .HTTPResponceUtil import HTTPResponceUtility

from .config.PROTOCOL import HEADER, ENCODING


class ClientService :

    def __init__(self, conn) -> None:
        self.conn = conn


    def serve_client(self, sock) -> None :
        self.sock = sock
        conn_active = True

        # Create chat service for each session
        self.chat_service = ChatService(self.conn)

        # Create HTTP responce object for each session
        self.responce_util = HTTPResponceUtility(sock)

        while conn_active :
            # Accept HTTP request
            self.accept_request()

            # Check for mistakes in header
            header_ok = self.deconstruct_header()

            if header_ok :
                # Serve client
                self.handle_request()
            else :
                conn_active = False
        
        self.sock.close()


    def accept_request(self) -> None :
        # Set header
        self.header = self.sock.recv(HEADER).decode(ENCODING)


    def deconstruct_header(self) -> int:
        try :
            request, URI, protocol = self.header.split(' ')[:3]
            
            self.request = request
            self.URI = URI
            self.protocol = protocol.split('\r')[0]

            # End session if protocol unknown
            if self.protocol == 'HTTP/1.1' or self.protocol == 'HTTP/2.0' :
                return 1
            else :
                print(f'[UNKNOWN] Protocol "{self.protocol}" unknown.')
                return 0

        except Exception as e :
            print(f'[EXCEPTION] {e}')
            return 0
            
        
    def handle_request(self) -> None :        
        if self.request == 'GET' :
            self.serve_GET()
        elif self.request == 'POST' :
            self.serve_POST()
        else :
            print(f'[UNKNOWN] Request method "{self.request}" unknown.')
    

    def serve_GET(self) -> None :
        input_, CODE = self.chat_service.get_users()
        input_length = bytes(str(len(input_)), "utf8")

        if (CODE == 200): 
            self.responce_util.send_success_response(input_, input_length)
            print(f"[CODE_200] resource {self.URI} sent")
        elif (CODE == 404): 
            self.responce_util.send_resource_not_found(input_, input_length)
            print(f"[CODE_404] resource {self.URI} not found")


    def serve_POST(self) :
        pass