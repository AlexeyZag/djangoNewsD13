from celery.app import shared_task
import time
from django.core.mail import send_mail
@shared_task
def hello():
    time.sleep(2)
    print('helooooooooooooooo')
@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)
