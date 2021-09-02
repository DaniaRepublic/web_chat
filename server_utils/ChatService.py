import sys
from sqlalchemy.sql import text

# add projects root folder to path
sys.path.append('../web_chat_git')


class ChatService :

    def __init__(self, conn) -> None:
        self.conn = conn
        self.chats_header = '''
        <!DOCTYPE html>
            <html>
                <head>
                    <title>Chats page</title>
                </head>
                <body>
        '''
        self.chats_bottom = '''
                </body>
            </html>
        '''
        self.msg_field = '''
        <div class='message_field'>
            <form method="POST" class="form" onsubmit="return check_input()">
                    <input type="text" id="message" name="message" class="send text" minlength="1">
                    <input type="submit" value="Send" class="send button">
            </form>
        </div>
        '''
        self.chats_script = '''
        <script>
            var msgs_field = document.getElementById("messages");
            msgs_field.scrollTop = msgs_field.scrollHeight;

            function check_input() {
                var msg = document.getElementById("message").value;
                if ((msg.replace(/ /g, '') != '') && msg) {
                    return true;
                }
                return false;
            }
        </script>
        '''
        self.chats_style = '''
        <style>
        html, body {
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
        }

        .chat {
            height: 98%;
            width: 50%;
            margin: auto;
            border: 3px solid antiquewhite;
            border-radius: 4px;
            box-sizing: border-box;
            display: flex;
            flex-flow: column;
        }

        .chat > div {
            flex: 1 1 auto;
        }

        .messages {
            overflow-y: scroll;
            height: calc(100vh - 8vh);
            background-color: ghostwhite;
        }

        .message_field {
            text-align: right;
            padding: 2% 3%;
            background-color: antiquewhite;
        }

        .my_name, .my_msg {
            text-align: right;
            font-weight: 100;
            margin: 2% 0;
        }

        .my_name {
            text-decoration: underline #659065 1.6px;
        }

        .not_my_name, .not_my_msg {
            text-align: left;
            font-weight: 100;
            margin: 2% 0;
        }

        .not_my_name {
            text-decoration: underline #956095 1.6px;
        }

        .user_msg {
            margin-right: 2%;
            margin-left: 16%;
        }

        .not_user_msg {
            margin-right: 16%;
            margin-left: 2%;
        }

        .form {
            height: 100%;
        }

        .send {
            margin: 0;
            padding: 0;
            height: 100%;
        }

        .text {
            width: 75%;
            margin-right: 5%;
            border: none;
            border-radius: 2px;
        }

        .button {
            width: 15%;
            background-color: white;
            border: none;
            border-radius: 2px;
        }
        </style>
        '''
        

    def get_chats_html(self, chats_ids : list) -> str :
        chats = []
        query = text('SELECT `id`, `name` FROM `chat` WHERE `id`=:id;')
        for chat_id in chats_ids :
            chats.append(self.conn.execute(query, {'id': chat_id}).fetchone())

        html = ''
        for chat in chats :
            chat_html = f'''
            <div class='one-of-chats'>
                <a href="/chat/{chat[0]}">
                    <h3>{chat[1]}<h3>
                </a>
            </div>
            '''
            html += chat_html

        return self.chats_header + html + self.chats_bottom

    
    def get_chat_html(self, chat_id : int, user_id : int) -> str :
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
        html =  "<div class='chat'><div class='messages' id='messages'>"
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
                <h3 class='{text_class}'>{ msg[3] }</h2>
            </div>
            <br>
            '''

            html += msg_html
        
        html += '</div>' + self.msg_field + '</div>'
        
        return self.chats_header + self.chats_style + html + self.chats_script + self.chats_bottom

    
    def save_message(self, chat_id, user_id, msg_text) :
        query = text('INSERT INTO `message` (`chat_id`, `user_id`, `text`) VALUES (:chat_id, :user_id, :text);')
        self.conn.execute(query, {'chat_id': chat_id, 'user_id': user_id, 'text': msg_text})
