class Winnie32APIError(Exception):
    """
    The base class for all exceptions in winnie32api
    """

class WinAPIError(Winnie32APIError):
    """
    Represents an error in win API
    """
    def __init__(self, msg: str, code: int):# pylint: disable=super-init-not-called
        self.msg = msg
        self.code = code

    def __str__(self) -> str:
        return f"{self.msg}. Status code: {self.code}"

class NotifError(Winnie32APIError):
    """
    The base class for notification-related exceptions
    """

class ManagerAlreadyExistsError(NotifError):
    """
    An error raised when tried to create more than one manager
    """
    def __str__(self) -> str:
        return "notification manager has already been defined for this app"
