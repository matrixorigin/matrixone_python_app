import pymysql


class MOClient(object):
    """
        Representation of a cli with a mo server using pymysql.

        Establish a connection to the MatrixOne database. Accepts several
        arguments:
        :param host: Host where the database server is located.
        :param user: Username to log in as.
        :param password: Password to use,
        :param database: Database to use, None to not use a particular one.
        :param port: MatrixOne port to use, default is usually OK. (default: 6001)
    """
    def __init__(self, host, user, password, database, port=6001):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.database = database

    def __enter__(self):
        self.db = pymysql.connect(host=self.host,
                                  port=self.port,
                                  user=self.user,
                                  passwd=self.password,
                                  database=self.database,
                                  charset='utf8mb4',
                                  connect_timeout=60,
                                  read_timeout=60,
                                  write_timeout=120,
                                  )
        self.db_cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.db_cursor.close()
            self.db.close()
        except AttributeError:
            print("db close failed")
            return True
