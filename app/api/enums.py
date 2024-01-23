from enum import Enum


class DeviceType(Enum):
    """设备类型

    Args:
        Enum (_type_): _description_
    """
    VTS = 1 # 竖屏触摸屏
    LTS = 2 # 横屏触摸屏
    VADS = 3 # 竖屏广告屏
    LADS = 4 # 横屏广告屏