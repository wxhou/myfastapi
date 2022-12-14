class UserNotExist(Exception):
    """ 用户不存在 """

    def __init__(self, msg: str = "用户不存在"):
        self.msg = msg

class UserNotActive(Exception):
    """用户未激活"""

    def __init__(self, msg: str = "用户未激活"):
        self.msg = msg

class PermissionError(Exception):
    """无访问权限"""

    def __init__(self, msg: str = "无访问权限"):
        self.msg = msg


class TokenExpiredError(Exception):
    def __init__(self, msg: str = "Token已过期"):
        self.msg = msg


class DeviceNotFound(Exception):
    """ 设备不存在 """

    def __init__(self, *args: object, msg: str = "设备不存在"):
        self.msg = msg
        super().__init__(*args)

class InvalidSystemClock(Exception):

    def __init__(self, *args: object, msg='系统时钟异常') -> None:
        self.msg = msg
        super().__init__(*args)