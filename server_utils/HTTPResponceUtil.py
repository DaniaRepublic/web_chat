class HTTPResponceUtility :

    def __init__(self, sock) -> None:
        self.sock = sock


    def send_success_response(self, body, body_length) -> None:
        responce_header = b'HTTP/1.1 200 OK\t\nContent-type: text/html; charset=utf-8\t\nContent-Length: ' + \
                        body_length + b'\t\n\n'

        self.sock.send(responce_header + body)


    def send_resource_not_found(self, body, body_length) -> None:
        responce_header = b'HTTP/1.1 404 ResourceNotFound\t\nContent-type: text/html; charset=utf-8\t\nContent-Length: ' + \
                        body_length + b'\t\n\n'  
                        
        self.sock.send(responce_header + body)