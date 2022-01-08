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
    new_post_links = ['http://127.0.0.1:8000/post/{0}/'.format(x.slug)+'\n' for x in new_posts]
    msg = '\n'.join(new_post_links)
    [send_mail(
        'У нас новые посты',
        msg,
        'x.Spirlhark.x@gmail.com',
        [contact.email],
        fail_silently=False,) for contact in Contact.objects.all() if len(new_posts) != 0]
