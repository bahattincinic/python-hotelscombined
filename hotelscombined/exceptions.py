class QueryException(Exception):

    def __init__(self, message, errors=None, status_code=None):
        super(QueryException, self).__init__(message)
        self.errors = errors
        self.status_code = status_code
