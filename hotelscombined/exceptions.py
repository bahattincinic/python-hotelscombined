class TokenException(Exception):
    pass


class QueryException(Exception):

    def __init__(self, message, errors=None):
        super(QueryException, self).__init__(message)
        self.errors = errors
