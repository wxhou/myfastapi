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


class AccessTokenFail(Exception):
    """ 访问令牌失败 """

    def __init__(self, msg: str = "访问令牌失败"):
        self.msg = msg

class NotAuthenticated(Exception):
    def __init__(self, msg: str = "JWT验证失败"):
        self.msg = msg


class DeviceNotFound(Exception):
    """ 设备不存在 """

    def __init__(self, msg: str = "设备不存在"):
        self.msg = msg