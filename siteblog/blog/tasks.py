from django.core.mail import send_mail
from siteblog.celery import app

from .service import send
from .models import Contact


@app.task
def send_spam_email(user_email):
    send(user_email)
