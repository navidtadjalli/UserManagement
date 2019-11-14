class APIException(Exception):
    status_code = None
    field = None
    message = None
    payload = None

    def __init__(self):
        Exception.__init__(self)

    def to_dict(self):
        rv = dict()

        if self.field:
            rv[self.field] = [self.message]
        elif self.payload:
            rv = self.payload
        else:
            rv['error'] = self.message

        return rv
