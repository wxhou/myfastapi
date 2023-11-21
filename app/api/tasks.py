import os
from app.settings import settings
from app.core.celery_app import celery
from app.utils.times import now, datetime, timedelta


@celery.task()
def hello_celery(name):
    return f'hello {name}'



@celery.task
def delete_old_text2audio():
    days_threshold = 7

    threshold_date = now() - timedelta(days=days_threshold)

    audio_dir = os.path.join(settings.UPLOAD_MEDIA_FOLDER, 'navigation')
    for file in os.listdir(audio_dir):
        _file = os.path.join(audio_dir, file)
        modified_time = datetime.fromtimestamp(os.path.getmtime(_file))
        if os.path.isfile(_file) and modified_time < threshold_date:
            os.remove(_file)
