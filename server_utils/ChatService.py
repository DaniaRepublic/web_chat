import sys

# setting path
sys.path.append('../web_chat')

from classes import User, DateTime


class ChatService :

    def __init__(self, conn) -> None:
        self.conn = conn


    def get_users(self) :
        res = self.conn.execute(f'SELECT id, name, reg_date FROM `user`;')

        users = []
        for row in res :
            user = User(row[0], row[1], row[2])
            users.append(user)

        html = ''
        for user in users :
            user_html = f'<h2>{user.get_name()}</h2>\n\
                <h3>Id: {user.get_id()}</h3>\n\
                <h3>Reg. date: {user.get_reg_date()}</h3>\n\
                <br>'
            html += user_html

        html = bytes(html, 'utf8')

        return html, 200
        