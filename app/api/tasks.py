from app.core.celery_app import celery



@celery.task
def hello_celery(name):
    return f'hello {name}'