from typing import Optional, Union, List, Literal
from pydantic import BaseModel, Field, IPvAnyNetwork


class DeviceInsert(BaseModel):
    """新建设备"""
    device_name: str = Field(description='设备名称', max_length=32)
    device_type: Literal[1,2,3] = Field(description='设备分类\n1触摸屏2广告机')
    device_number: Optional[str] = Field(default=None, description='设备编号', max_length=64)
    device_position: Optional[str] = Field(default=None, description='设备位置', max_length=64)
    device_screen_type: Literal[1,2] = Field(description='屏幕分类\n1竖屏2横屏')
    device_screen_number: Optional[str] = Field(default=None, description='设备屏幕编号', max_length=64)
    device_mac_addr: str = Field(description='设备Mac', max_length=64, pattern=r'[A-Fa-f0-9:]{17}')
    device_ip_addr: IPvAnyNetwork = Field(description='设备IP', )
    annotation: Optional[str] = Field(default=None, description='备注', max_length=32)


class DeviceUpdate(BaseModel):
    """更新设备"""
    device_name: str = Field(default=None, description='设备名称', max_length=32)
    device_type: Literal[1,2] = Field(default=None, description='设备分类\n1竖屏2横屏')
    device_position: Optional[str] = Field(default=None, description='设备位置', max_length=64)
    device_number: Optional[str] = Field(default=None, description='设备编号', max_length=64)
    device_screen_number: Optional[str] = Field(default=None, description='设备屏幕编号', max_length=64)
    device_mac_addr: str = Field(default=None, description='设备Mac', max_length=64, pattern=r'[A-Fa-f0-9:]{17}')
    device_ip_addr: IPvAnyNetwork = Field(default=None, description='设备IP')
    annotation: Optional[str] = Field(default=None, description='备注', max_length=32)


class DeviceRegister(BaseModel):
    """设备注册"""
    device_register_code: str = Field(description='设备序列号', max_length=64)
    device_app_version: str = Field(description='设备名称', pattern=r'[Vv0-9.]{5,7}')
