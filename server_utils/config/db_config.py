from sqlalchemy import create_engine


class DBConnector :

    def __init__(self) -> None :
        try :
            self.engine = create_engine(
                'mysql+pymysql://<user>:<password>@localhost/<db>', 
                isolation_level="READ COMMITTED",
                pool_size=8
            )

        except Exception as e :
            print(e)
            exit('Database connection failed')


    def connect(self) :
        return self.engine.connect()


    def execute(self, query : str, args=None) -> None :
        if args :
            self.conn.execute(query, args)
        else :
            self.conn.execute(query)


    def commit(self) -> None :
        self.conn.commit()

    
    def fetchall(self) -> list :
        return self.conn.fetchall()


    def fetchone(self) -> tuple :
        return self.conn.fetchone()


    def close(self) -> None :
        self.conn.close()
        self.engine.close()


