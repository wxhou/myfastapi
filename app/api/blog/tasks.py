from app.core.celery_app import celery


@celery.task(acks_late=True)
def helloworld(x, y):
    print("hello world")
    return x + y