import tushare as ts


class TuShareClient(object):
    """
        Representation of a cli with a tushare server.

        Establish a connection to the TuShare. Accepts several
        arguments:
        :param token: Your tushare api token
    """
    def __init__(self, token):
        self.token = token

    def __enter__(self):
        ts.set_token(self.token)
        self.apiCli = ts.pro_api()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
