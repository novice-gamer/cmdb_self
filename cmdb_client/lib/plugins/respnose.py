class BaseResponse(object):
    def __init__(self):
        self.status = True
        self.data = None
        self.error = None

    @property
    def dict(self):
        return self.__dict__
