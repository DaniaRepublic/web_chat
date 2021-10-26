import sys
from sqlalchemy.sql import text

# add projects root folder to path
sys.path.append('../web_chat_git')

from classes import User


class LoginService :

    def __init__(self) -> None:
        self.user_logged_in = False
        self.get_static_content = lambda tag_name, f_path : f'''
        <{ tag_name }>
        {
            open(f'static/{f_path}', 'r').read()
        }
        </{ tag_name }>
        '''
        

    def get_html(self, prefix) -> str :
        return f'''
            <!DOCTYPE html>
            <html>
                <head>
                    <title>Register page</title>
                </head>
                <body>
                    {self.get_static_content("style", "css/login.css")}
                    <div class="wrapper">
                        <div class="center-block">
                            {''.join([f'<h3>{prefix}</h3>' for _ in [1] if prefix])}
                            <form method="POST">
                                <label for="name">Name</label><br>
                                <input type="text" id="name" name="name"><br><br>
                                <label for="pass">Password</label><br>
                                <input type="text" id="pass" name="pass"><br><br>
                                <input type="submit" id="submit" value="SUBMIT">
                            </form>
                        </div>
                    </div>
                </body>
            </html>
            '''


    def login(self, conn, name, password) -> bool :
        query = text('SELECT * FROM `user` WHERE `name`=:name AND `password`=:password;')
        params = {
            'name': name, 
            'password': password
        }
        res = conn.execute(query, **params).fetchone()

        if res :
            self.user = User(res[0], name, res[6], res[4], [int(_) for _ in res[1].split(' ')], res[5])
            self.user_logged_in = True
            return True
        
        return False