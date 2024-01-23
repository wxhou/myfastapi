from sqlalchemy import Column, String, Integer, SmallInteger, DateTime, Boolean, Enum
from app.api.model import Base
from app.api.enums import DeviceType


class DeviceInfo(Base):
    """设备信息
    """
    __tablename__ = 't_device_info'

    id = Column(Integer, primary_key=True)
    device_register_code = Column(String(32))  # 设备注册码 注册时自动生成
    device_name = Column(String(64))  # 设备名称
    device_code = Column(String(64), nullable=False)  # 设备唯一编号
    device_type = Column(Enum(DeviceType), nullable=False, index=True)  # 设备类型  1:竖屏 2:横屏 3:广告横屏 4:广告竖屏
    device_position = Column(String(64))  # 设备位置
    device_screen_type = Column(SmallInteger, nullable=False) # 屏幕类型 1竖屏  2横屏
    device_screen_number = Column(String(64))  # 设备屏幕编号
    device_app_version = Column(String(64))  # 设备APP相关版本号
    device_mac_addr = Column(String(64))  # 设备mac地址
    device_ip_addr = Column(String(32))  # 设备ip地址
    annotation = Column(String(128))  # 备注信息

    is_registered = Column(Boolean, nullable=False, default=False)  # 设备是否注册 1: 已注册 0：未注册
    register_time = Column(DateTime, default='2012-01-01 00:00:00')

    def generate_register_code(self, device_type, id):
        self.device_register_code = "JL%.2d%.3d" % (device_type, id)
