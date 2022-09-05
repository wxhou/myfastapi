class UserNotExist(Exception):
    """ 用户不存在 """

    def __init__(self, msg: str = "用户不存在"):
        self.msg = msg

class UserNotActive(Exception):
    """用户未激活"""

    def __init__(self, msg: str = "用户未激活"):
        self.msg = msg


class AccessTokenFail(Exception):
    """ 访问令牌失败 """

    def __init__(self, msg: str = "访问令牌失败"):
        self.msg = msg
