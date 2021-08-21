from sqlalchemy import create_engine


class DBConnector :

    def __init__(self) -> None:
        try :
            self.engine = create_engine('mysql+pymysql://<user>:<PASS>;@localhost/<DB_name>', pool_size=8)
        except Exception as e :
            print(e)
            exit('Database connection failed')


    def execute(self, query) :
        with self.engine.connect() as conn :
            return conn.execute(query)

