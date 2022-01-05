import datetime

from django.core.cache import cache

from .models import *
from django.core.mail import send_mail
from siteblog.celery import app

from .service import send


@app.task
def send_spam_email(user_email):
    send(user_email)


@app.task
def send_beat_email():
    new_posts = Post.objects.filter(created_at__date__gte=cache.get('last_send') or datetime.date.today())
    cache.set('last_send', datetime.date.today(), None)
    [send_mail(
        'У нас новые посты',
        'http://127.0.0.1:8000/post/{0}/'.format(x.slug),
        'x.Spirlhark.x@gmail.com',
        [contact.email],
        fail_silently=False,)for x in new_posts for contact in Contact.objects.all() if len(new_posts) != 0]
