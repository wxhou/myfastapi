import os
import hashlib
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request, File, UploadFile, Form
from app.api.deps import get_db
from app.core.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.common.decorator import async_to_sync
from app.utils.logger import logger
from app.utils.times import dt_strftime
from app.api.user.model import BaseUser, BasePermission
from .model import UploadModel
from .auth import get_current_active_user


router = APIRouter()


@router.post("/upload/", summary='上传文件')
async def create_upload_file(file: UploadFile = File(),
                             md5 = Form(..., description="文件MD5值"),
                             db:AsyncSession = Depends(get_db),
                             current_user: BaseUser = Depends(get_current_active_user)):
    """上传文件"""
    obj = await db.scalar(select(UploadModel).where(UploadModel.uniqueId==md5, UploadModel.status==0))
    if obj is not None:
        return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId'}))
    ext = os.path.splitext(file.filename)[1]
    if ext not in settings.ALLOWED_IMAGE_EXTENSIONS:
        return response_err(ErrCode.FILE_TYPE_ERROR)
    root_path = os.path.join(settings.UPLOAD_MEDIA_FOLDER, dt_strftime(fmt="%Y%m"))
    new_fname = "{}{}".format(uuid4(), ext)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    save_file = os.path.join(root_path, new_fname)
    # 计算文件MD5
    md5_obj = hashlib.md5()
    with open(save_file, 'wb+') as buffer:
        FileStream = await file.read()
        md5_obj.update(FileStream)
        buffer.write(FileStream)
    obj = await db.scalar(select(UploadModel).where(UploadModel.uniqueId==md5_obj.hexdigest(), UploadModel.status==0))
    if obj is not None:
        return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId'}))
    obj = UploadModel(fileUrl='/upload' + save_file.split(settings.UPLOAD_MEDIA_FOLDER)[1],
                      uniqueId=md5,
                      filename=file.filename,
                      content_type=file.content_type,
                      uid=current_user.id)
    db.add(obj)
    await db.commit()
    return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId'}))



@router.get("/routes", summary="所有路由", deprecated=True)
async def api_routes(request: Request,
                     db:AsyncSession = Depends(get_db)):
    result = []
    number = 1
    for route in request.app.routes:
        items = {
            "name": route.name,
            "path": route.path
        }
        result.append(items)
        obj = BasePermission(name=route.path, function_name=route.name, order_num=number)
        number += 1
        db.add(obj)
    await db.commit()
    return response_ok(data=result)


@router.get("/sync", summary="同步路由", deprecated=True)
def sync_routes(request: Request,
                db:AsyncSession = Depends(get_db)):
    ret = async_to_sync(request.body)()
    logger.info(ret)
    return response_ok()