import os
from sqlalchemy import delete, select
from app.core.celery_app import celery
from app.extensions import async_session
from app.common.decorator import sync_run_async
from app.api.base.model import UploadModel


@celery.task(acks_late=True, queue='celery')
@sync_run_async
async def verify_upload_file_is_exists(md5, save_file):
    is_exists = os.path.exists(save_file)
    if not is_exists:
        async with async_session() as session:
            sql = select(UploadModel).where(UploadModel.status==0, UploadModel.uniqueId==md5)
            obj = await session.scalar(sql)
            if obj:
                await session.delete(obj)
            await session.commit()
    return is_exists
