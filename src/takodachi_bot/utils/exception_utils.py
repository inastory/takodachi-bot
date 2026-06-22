class PermissionError(Exception):
    def __init__(self, message, code=None):
        super().__init__("Permission denied: " + message)
        self.code = code

class NoneService(Exception):
    pass