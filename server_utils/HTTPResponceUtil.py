class HTTPResponceUtility :

    def __init__(self, sock) -> None:
        self.sock = sock

    # 200s / Success
    def send_200_success_response(self, body, body_length) -> None :
        responce_header = b'HTTP/1.1 200 OK\t\nContent-type: text/html; charset=utf-8\t\nContent-Length: ' + \
                        body_length + b'\t\n\n'
        self.sock.send(responce_header + body)

    # 300s / Redirection
    def send_303_see_other(self, location) -> None :
        response_header = b'HTTP/1.1 303 See Other\t\nContent-type: text/html;\t\nLocation: ' + location
        print(response_header)
        self.sock.send(response_header)

    # 400s / Client Error
    def send_404_resource_not_found(self, body, body_length) -> None :
        responce_header = b'HTTP/1.1 404 ResourceNotFound\t\nContent-type: text/html; charset=utf-8\t\nContent-Length: ' + \
                        body_length + b'\t\n\n'   
        self.sock.send(responce_header + body)

    