import os
import edge_tts
from uuid import uuid4
from random import randint
from typing import Optional
from anyio import Path
from sqlalchemy import select
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi import Query, File, UploadFile, Form, Header
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
from .tasks import upload_file_task, verify_file_exist_task


router = APIRouter()


@router.post("/upload/", summary='上传文件')
async def create_upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(description='文件'),
    md5 = Form(..., description="文件MD5值"),
    db: AsyncSession = Depends(get_db),
    current_user: BaseUser = Depends(get_current_active_user)
):
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

    background_tasks.add_task(upload_file_task, file, save_file)
    await Path(save_file).write_bytes(await file.read())
    # 对比文件MD5
    obj = UploadModel(fileUrl='/upload' + save_file.split(settings.UPLOAD_MEDIA_FOLDER)[1],
                      uniqueId=md5,
                      filename=file.filename,
                      content_type=file.content_type,
                      uid=current_user.id)
    db.add(obj)
    await db.commit()
    verify_file_exist_task.apply_async(args=(md5, save_file), eta=now(utc=1) + timedelta(seconds=60))
    return response_ok(data=obj.to_dict(exclude={'status', 'uniqueId', 'uid'}))



@router.get("/text/audio", summary="文本转语音")
async def text_to_audio(
    text: str = Query(..., example='你好哟，我是智能语音助手，小布', max_length=500),
    lang: str = Query(default='zh', description="选择语言\nzh中文|en英文", pattern=r'zh|en'),
    model: str = Query(default=None, description='选择模型\nedge|pyttsx3', pattern=r'edge|pyttsx3'),
    redis: AsyncRedis = Depends(get_redis)
):

    VOICE = settings.EDGE_VOICE_LANG[lang]

    audio_dir = os.path.join(settings.UPLOAD_MEDIA_FOLDER, 'navigation')
    if not os.path.exists(audio_dir):
        os.makedirs(audio_dir)
    res = await redis.get(VOICE + text)
    if res and os.path.exists(res.decode()):
        logger.info("VOICE IS: {}".format(res))
        await redis.expire(VOICE + text, randint(6*24*60*60, 7*24*60*60))
        return FileResponse(res, media_type="audio/mpeg")

    FILE_NAME = f"{uuid4()}.mp3"
    OUTPUT_FILE = os.path.join(audio_dir, FILE_NAME)

    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(OUTPUT_FILE)
    logger.info("OUTPUT_FILE: {}".format(os.path.basename(OUTPUT_FILE)))
    await redis.set(VOICE + text, OUTPUT_FILE, ex=randint(6*24*60*60, 7*24*60*60))
    return FileResponse(OUTPUT_FILE, media_type="audio/mpeg")


@router.get("/routes", summary="所有路由", deprecated=True)
async def api_routes(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
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