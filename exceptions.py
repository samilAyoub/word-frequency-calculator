class GetRequestException(Exception):
    """Exception raised for get request errors

    Attributes:
        url -- url which caused the error
        message -- explanation of the error
    """

    def __init__(self, url, msg):
        self.url = url
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return f'Request Failed.\nURL:{self.url}\nMessage: {self.msg}'


class StoreResultException(Exception):
    """Exception raised for store result errors

    Attributes:
        result -- result we attempt to store
        message -- explanation of the error
    """

    def __init__(self, result, msg):
        self.result = result
        self.msg = msg
        super().__init__(msg)

    def __str__(self):
        return f'Error while storing the result.\nResult:{self.result}\nMessage: {self.msg}'
