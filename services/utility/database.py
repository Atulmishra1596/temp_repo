from psycopg2 import pool
import psycopg2
from sqlalchemy import create_engine  
from utility.utilconfig import dbconfig

class PostGres():
    def __init__(self):
        self.params = dbconfig(section='postgresql')

        self.conn = create_engine("postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}".format(
                                        user=self.params['user'],password=self.params['password'], 
                                        host=self.params['host'],port=self.params['port'], database=self.params['database']))

        self.threaded_postgreSQL_pool = pool.ThreadedConnectionPool(1, 10, user=self.params['user'], 
                                            password=self.params['password'], host=self.params['host'], 
                                            port=self.params['port'], database=self.params['database'])

    def create_connection(self):
        try:
            return self.threaded_postgreSQL_pool.getconn()
        except:
            raise psycopg2.DatabaseError('Error while connecting to PostgreSQL')
    def connect(self):
        self.connection = psycopg2.connect(**self.params)
        self.cursor = self.connection.cursor()
        return self.cursor

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()