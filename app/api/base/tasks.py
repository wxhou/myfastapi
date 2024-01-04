import os
from anyio import Path
from sqlalchemy import select
from fastapi import UploadFile
from app.core.celery_app import celery
from app.extensions import session
from app.api.base.model import UploadModel


async def upload_file_task(file: UploadFile, save_file):
    """上传文件
    fastapi background task
    """
    # with open(save_file, 'rb') as f:
    #     f.write(file.file)
    await Path(save_file).write_bytes(await file.read())


@celery.task(acks_late=True, queue='celery')
def verify_file_exist_task(md5, save_file):
    """验证文件是否存在"""
    is_exists = os.path.exists(save_file)
    if not is_exists:
        with session() as db:
            obj = db.scalar(select(UploadModel).where(UploadModel.status==0, UploadModel.uniqueId==md5))
            if obj:
                db.delete(obj)
            db.commit()
    return is_exists
