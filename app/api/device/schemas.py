from typing import Optional, Union, List, Literal
from pydantic import BaseModel, Field, IPvAnyNetwork


class DeviceInsert(BaseModel):
    """新建设备"""
    device_name: str = Field(title='设备名称', max_length=32)
    device_type: Literal[1,2,3] = Field(title='设备分类', description='1触摸屏2广告机')
    device_number: Optional[str] = Field(default=None, title='设备编号', max_length=64)
    device_position: Optional[str] = Field(default=None, title='设备位置', max_length=64)
    device_screen_type: Literal[1,2] = Field(title='屏幕分类', description='1竖屏2横屏')
    device_screen_number: Optional[str] = Field(default=None, title='设备屏幕编号', max_length=64)
    device_mac_addr: str = Field(title='设备Mac', max_length=64, regex=r'[A-Fa-f0-9:]{17}')
    device_ip_addr: IPvAnyNetwork = Field(title='设备IP', )
    annotation: Optional[str] = Field(default=None, title='备注', max_length=32)


class DeviceModify(BaseModel):
    """修改设备"""
    id: int = Field(title='设备ID', ge=1)
    device_name: str = Field(default=None, title='设备名称', max_length=32)
    device_type: Literal[1,2] = Field(default=None, title='设备分类', description='1竖屏2横屏')
    device_position: Optional[str] = Field(default=None, title='设备位置', max_length=64)
    device_number: Optional[str] = Field(default=None, title='设备编号', max_length=64)
    device_screen_number: Optional[str] = Field(default=None, title='设备屏幕编号', max_length=64)
    device_mac_addr: str = Field(default=None, title='设备Mac', max_length=64, regex=r'[A-Fa-f0-9:]{17}')
    device_ip_addr: IPvAnyNetwork = Field(default=None, title='设备IP')
    annotation: Optional[str] = Field(default=None, title='备注', max_length=32)


class DeviceDelete(BaseModel):
    id: int = Field(title='设备ID', ge=1)


class DeviceRegister(BaseModel):
    """设备注册"""
    device_register_code: str = Field(title='设备序列号', max_length=64)
    device_app_version: str = Field(title='设备名称', regex=r'[Vv0-9.]{5-7}')
