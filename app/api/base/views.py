import os
import edge_tts
from uuid import uuid4
from typing import Optional
from anyio import Path
from sqlalchemy import select
from fastapi import APIRouter, Depends, Request, Query, File, UploadFile, Form, Header
from fastapi.responses import FileResponse
from app.extensions import get_db, get_redis, AsyncSession, AsyncRedis
from app.settings import settings
from app.common.response import ErrCode, response_ok, response_err
from app.common.decorator import async_to_sync
from app.utils.logger import logger
from app.utils.times import dt_strftime, now, timedelta
from app.api.user.model import BaseUser, BasePermission
from .model import UploadModel
from .schemas import InputText
from .auth import get_current_active_user
from .tasks import verify_upload_file_is_exists


router = APIRouter()


@router.post("/upload/", summary='上传文件')
async def create_upload_file(db: AsyncSession = Depends(get_db),
                             file: UploadFile = File(),
                             md5 = Form(..., description="文件MD5值"),
                             current_user: BaseUser = Depends(get_current_active_user)):
    """上传文件"""
    obj = await db.scalar(select(UploadModel).where(UploadModel.uniqueId==md5, UploadModel.status==0))
    if obj is not None:
        return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId'}))
    ext = os.path.splitext(file.filename)[1]
    if ext not in settings.ALLOWED_EXTENSIONS:
        return response_err(ErrCode.FILE_TYPE_ERROR)
    root_path = os.path.join(settings.UPLOAD_MEDIA_FOLDER, dt_strftime(fmt="%Y/%m"))
    new_fname = "{}{}".format(uuid4(), ext)
    if not os.path.exists(root_path):
        os.makedirs(root_path)
    save_file = os.path.join(root_path, new_fname)
    # 异步上传文件1
    # async with aiofiles.open(save_file, 'wb+') as fp:
    #     while content := await file.read(1024):
    #         logger.info(content)
    #         await fp.write(content)
    # 异步上传文件2
    await Path(save_file).write_bytes(await file.read())

    # 同步上传文件
    # with open(save_file, 'wb+') as buffer:
    #     buffer.write(await file.read())
    # 对比文件MD5
    obj = UploadModel(fileUrl='/upload' + save_file.split(settings.UPLOAD_MEDIA_FOLDER)[1],
                      uniqueId=md5,
                      filename=file.filename,
                      content_type=file.content_type,
                      uid=current_user.id)
    db.add(obj)
    await db.commit()
    verify_upload_file_is_exists.apply_async(args=(md5, save_file), eta=now(utc=1) + timedelta(seconds=60))
    return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId', 'uid'}))



@router.get("/text/audio", summary="文本转语音")
async def text_to_audio(text: str = Query(default='你好哟，我是智能语音助手，小布', max_length=500, description='合成的文本'),
                        redis: AsyncRedis = Depends(get_redis)):

    VOICE = "zh-CN-XiaoxiaoNeural"
    audio_dir = os.path.join(settings.UPLOAD_MEDIA_FOLDER, 'navigation')
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    res = await redis.get(VOICE + text)
    if res:
        logger.info("VOICE IS: {}".format(res))
        return FileResponse(res, media_type="audio/mpeg")

    FILE_NAME = f"{uuid4()}.mp3"
    OUTPUT_FILE = os.path.join(audio_dir, FILE_NAME)

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)
    logger.info("OUTPUT_FILE: {}".format(os.path.basename(OUTPUT_FILE)))
    await redis.set(VOICE + text, OUTPUT_FILE, ex=24*60*60)
    return FileResponse(OUTPUT_FILE, media_type="audio/mpeg")


@router.get("/routes", summary="所有路由", deprecated=True)
async def api_routes(request: Request,
                     db: AsyncSession = Depends(get_db)):
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
def sync_routes(user_agent: Optional[str] = Header(...)):
    return response_ok(data=user_agent)