import pymysql
import dotenv
import os


path_to_env = os.path.join(os.getcwd(), '.env')
dotenv.load_dotenv(dotenv_path=path_to_env)


dbconfig = {
'host': os.getenv('HOST'),
'user': os.getenv('USER'),
'password': os.getenv('PASSWORD'),
'database': os.getenv('DATABASE'),
}

class DBConnector:

    def __init__(self, dbconfig: dict):
        self._dbconfig = dbconfig
        self._connection = self._set_connection()
        self._cursor = self._set_cursor()

    def _set_connection(self):
        connection = pymysql.connect(**self._dbconfig)
        return connection

    def _set_cursor(self):
        cursor = self._connection.cursor()
        return cursor

    def get_connection(self):
        return self._connection

    def get_cursor(self):
        return self._cursor

    def close(self):
        if self._connection.open:
            self._cursor.close()
            self._connection.close()


