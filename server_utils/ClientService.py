import sys
from urllib.parse import parse_qs

# add projects root folder to path
sys.path.append('../web_chat_git')

from .ChatService import ChatService
from .LoginService import LoginService
from .HTTPResponceUtil import HTTPResponceUtility

from .config.PROTOCOL import HEADER, ENCODING


class ClientService :

    def __init__(self, conn, addr) -> None:
        self.conn = conn
        self.addr = addr
        self.redirect_to_page = lambda uri : f'''
        <!DOCTYPE html>
        <html>
        <head>
            <meta http-equiv="refresh" content="0; URL=http://{ addr[0] }:{ addr[1] }{ uri }" />
        </head>
        </html>
        '''


    def serve_client(self, sock) -> None :
        self.sock = sock

        # Create login service for each session
        self.login_service = LoginService()
        #
        # *** Temporary for saving time on login ***
        #
        #self.login_service.login(self.conn, 'Ivan', 'password123')

        # Create chat service for each session
        self.chat_service = ChatService(self.conn)

        # Create HTTP responce object for each session
        self.responce_util = HTTPResponceUtility(sock)

        while True :
            # Accept HTTP request
            self.accept_request()
            if len(self.header) == 0  :
                continue

            # Check for mistakes in header
            header_ok = self.deconstruct_header()

            if header_ok :
                # Serve client
                self.handle_request()
            else :
                break
        
        print("client served")
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
    

    def serve_GET(self, content="", redirect=None, serve_raw=False) -> None :
        if serve_raw :
            input_, CODE = bytes(content, 'utf8'), 200

        elif redirect :
            input_, CODE = bytes(self.redirect_to_page(redirect), 'utf8'), 200    
          
        # In the following set of conditions, each condition
        # specifies a page of an application.
        elif self.URI == '/login' or self.URI == '/':
            input_, CODE = bytes(self.login_service.get_html(content), 'utf8'), 200

        # page with chats and selected chat
        # url: /home</n: int>
        elif self.URI.split('/')[1] == 'home':
            if self.login_service.user_logged_in :
                input_, CODE = bytes(self.chat_service.get_home(self.login_service.user.chats_ids), 'utf8'), 200  
            else :
                # Redirect unauthorized user to /login URI
                input_, CODE = bytes(self.redirect_to_page('/login'), 'utf8'), 200      
        
        ###
        # !!! NEEDS TO BE IMPLEMENTED IN AJAX !!!
        # choosing chat from chats menu
        ###
        
        elif self.URI.split('/')[1] == 'chat' :
            if self.login_service.user_logged_in :
                try :
                    # Check if chat_id given in uri is an integer
                    chat_id = int(self.URI.split('/')[2])
                    # Check if user is a member of chat with that id
                    if chat_id in self.login_service.user.get_chats_ids() :
                        input_, CODE = bytes(self.chat_service.get_chat_msgs_html(chat_id, self.login_service.user.get_id()), 'utf8'), 200
                    else :
                        input_, CODE = bytes(f'<h3>URI "{self.URI}" is not accessable.</h3>', 'utf8'), 404
                except Exception as e :
                    print(f'[EXCEPTION] {e}')
                    input_, CODE = bytes(f'<h3>URI "{self.URI}" unknown.</h3>', 'utf8'), 404
            else :
                # Redirect unauthorized user to /login URI
                input_, CODE = bytes(self.redirect_to_page('/login'), 'utf8'), 200

        else :
            input_, CODE = bytes(f'<h3>URI "{self.URI}" unknown.</h3>', 'utf8'), 404
        
        # Compute length of html that will be sent 
        input_length = bytes(str(len(input_)), "utf8")

        # Send according to status code
        if (CODE == 200): 
            self.responce_util.send_200_success_response(input_, input_length)
            print(f'[CODE_200] resource {self.URI} sent')
        elif (CODE == 404): 
            self.responce_util.send_404_resource_not_found(input_, input_length)
            print(f'[CODE_404] resource {self.URI} not found')


    def serve_POST(self) -> None :
        try :
            values_enc = self.header.split('\n')[-1]
            values_dict = parse_qs(values_enc)
        except Exception as e :
            print(f'[EXCEPTION] [in making variables dictionary] {e}')
            return

        if self.URI == '/login' or self.URI == '/':
            try :
                name = values_dict['name'][0]
                password = values_dict['pass'][0]
                if self.login_service.login(self.conn, name, password) :
                    #self.URI = '/home'
                    self.serve_GET(redirect="/home")
                else :
                    self.serve_GET(content='Wrong name or password.')
            except Exception as e :
                print(f'[EXCEPTION] [in /login POST] {e}')
                self.serve_GET()
                return

        elif self.URI.split('/')[1] == 'chat' :
            if self.login_service.user_logged_in :
                try :
                    message = values_dict['message'][0]
                    # Check if chat_id given in uri is an integer
                    chat_id = int(self.URI.split('/')[2])
                    # Check if user is a member of chat with that id
                    if chat_id in self.login_service.user.get_chats_ids() :
                        your_new_message = self.chat_service.save_message(chat_id, self.login_service.user.get_id(), message)
                        # send back your new message
                        self.serve_GET(content=your_new_message, serve_raw=True)
                except Exception as e :
                    print(f'[EXCEPTION] {e}')
                    self.serve_GET()
                    return
                
        elif self.URI.split('/')[1] == 'home' :
            if self.login_service.user_logged_in :
                try :
                    message = values_dict['message'][0]
                    # Check if chat_id given in uri is an integer
                    chat_id = int(self.URI.split('/')[2])
                    # Check if user is a member of chat with that id
                    if chat_id in self.login_service.user.get_chats_ids() :
                        your_new_message = self.chat_service.save_message(chat_id, self.login_service.user.get_id(), message)
                        #self.serve_GET()
                        self.serve_GET(content=your_new_message, serve_raw=True)
                except Exception as e :
                    print(f'[EXCEPTION] [in /home POST] {e}')
                    self.serve_GET()
                    return