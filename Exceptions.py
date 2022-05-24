class CustomException(Exception):
    def __init__(self, message, details=None):
        super(CustomException, self).__init__(message)
        self.message = message
        self.details = details

    def __str__(self):
        if self.details is not None:
            return str(self.message) + "\n" + str(self.details)
        return str(self.message)


class ServerException(CustomException):
    def __init__(self):
        self.message = "Can not receive data from server"
        self.details = "Try another key or connect Internet)"


class IncorrectMatrixException(CustomException):
    def __init__(self):
        self.message = "Incorrect input matrix"
        self.details = "Can not parse matrix for one element"


class ComplexRootsException(CustomException):
    def __init__(self):
        self.message = "Some of the roots are complex"
        self.details = "Try different equation"


class GatewayException(CustomException):
    def __init__(self):
        self.message = "Gateway exception"
        self.details = "Try to reboot gateway"


class ParseException(CustomException):
    def __init__(self):
        self.message = "Parsing exception"
        self.details = "Please contact support: vip.zatebe@mail.ru"
