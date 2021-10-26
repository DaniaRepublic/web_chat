import sys
from sqlalchemy.sql import text

# add projects root folder to path
sys.path.append('../web_chat_git')


class ChatService :

    def __init__(self, conn) -> None:
        self.conn = conn
        self.get_static_content = lambda tag_name, f_path : f'''
        <{ tag_name }>
        { open(f'static/{f_path}', 'r').read() }
        </{ tag_name }>
        '''
        self.home_header = f'''
        <!DOCTYPE html>
        <html>
            <head>
                <title>Home page</title>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
            </head>
            <body>
            {self.get_static_content("style", "css/chat.css")}
            {self.get_static_content("style", "css/chats.css")}
            {self.get_static_content("style", "css/home.css")}
            <div class="chats_and_chat">
        '''
        self.home_bottom = f'''
            </div>
            {self.get_static_content("script", "js/chat.js")}
            {self.get_static_content("script", "js/select_chat_ajax.js")}
            </body>
        </html>
        '''
        self.msg_field = '''
        <div class='message_field'>
            <form method="POST" class="form">
                    <input type="text" id="message" name="message" class="send text" minlength="1">
                    <input type="submit" value="Send" class="send button">
            </form>
        </div>
        '''
        

    def get_chats_html(self, chats_ids : list) -> str :
        chats = []
        query = text('SELECT `id`, `name` FROM `chat` WHERE `id`=:id;')
        for chat_id in chats_ids :
            chats.append(self.conn.execute(query, {'id': chat_id}).fetchone())

        html = "<div class='chats'>"
        for chat in chats :
            chat_html = f'''
                <div class="one_of_chats" id="{chat[0]}">
                    <h3>{chat[1]}</h3>
                </div>
            '''
            html += chat_html

        html += '</div>'

        return html

    
    def get_chat_msgs_html(self, chat_id : int, user_id : int) -> str :
        html = "<div class='messages' id='messages'>"
        if (chat_id == -1) and (user_id == -1):
            return  html + '</div>' 

        # Get chat info
        query = text('SELECT * FROM `chat` WHERE `id`=:id;')
        res = self.conn.execute(query, {'id': chat_id}).fetchone()
        ID = res[0]
        users_ids = res[1].split(' ')
        name = res[2]
        description = res[3]

        # Get user names
        query = ''.join([f'`id`={users_id} OR ' for users_id in users_ids])
        usernames = self.conn.execute(f'SELECT `id`, `name` FROM `user` WHERE {query[:-4]};').fetchall()
        usernames_dict = {}
        for username in usernames :
            usernames_dict[username[0]] = username[1]

        # Get messages
        query = text('SELECT * FROM `message` WHERE `chat_id`=:chat_id ORDER BY `date` ASC;')
        msgs = self.conn.execute(query, {'chat_id': chat_id}).fetchall()

        # Create html
        for msg in msgs :
            msg_user_id = msg[2]

            if msg_user_id == user_id :
                msg_class = 'user_msg'
                name = 'You'
                name_class = 'my_name'
                text_class = 'my_msg'
            else :
                msg_class = 'not_user_msg'
                name = usernames_dict[msg_user_id]
                name_class = 'not_my_name'
                text_class = 'not_my_msg'

            msg_html = f'''
            <div class='{ msg_class }'>
                <h3 class='{name_class}'>{ name }</h3>
                <h3 class='{text_class}'>{ msg[3] }</h3>
            </div>
            <br>
            '''

            html += msg_html
        
        html += '</div>'
        
        # Return final html 
        return html
    

    def get_home(self, chats_ids : list) -> str :
        chats = self.get_chats_html(chats_ids)
        chat = "<div class='chat' id='chat'>" + self.get_chat_msgs_html(-1, -1) + self.msg_field + "</div>"
        return self.home_header + chats + chat + self.home_bottom

    
    def save_message(self, chat_id, user_id, msg_text) -> str :
        query = text('INSERT INTO `message` (`chat_id`, `user_id`, `text`) VALUES (:chat_id, :user_id, :text);')
        self.conn.execute(query, {'chat_id': chat_id, 'user_id': user_id, 'text': msg_text})
        return f''' 
            <div class='user_msg'>
                <h3 class='my_name'>You</h3>
                <h3 class='my_msg'>{ msg_text }</h3>
            </div>
            <br>
            '''
