import psycopg2

from resources.config import host, username, password, datasource


class Connect:

    def __init__(self, name):
        self.connection = psycopg2.connect(host=host, user=username, password=password, database=datasource)
        self.cursor = self.connection.cursor()
        self.name = name

    def commit(self):
        self.connection.commit()

    def finalize(self):
        self.cursor.close()
        self.connection.close()
        print("[INFO] Database connection terminated successfully! From " + self.name)