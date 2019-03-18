class MultipleObjectsReturned(Exception):
    def __init__(self, message='', errors=None):
        self.message = message
        self.errors = errors


class DoesNotExist(Exception):
    def __init__(self, message='', errors=None):
        self.message = message
        self.errors = errors

class DeleteError(Exception):
    def __init__(self, message='', errors=None):
        self.message = message
        self.errors = errors
