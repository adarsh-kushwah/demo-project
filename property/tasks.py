from celery import shared_task
import time


@shared_task
def testing_celery(x,y):
    print('_________------hello->')
    time.sleep(10)
    print('executed   ...')
    return x+y