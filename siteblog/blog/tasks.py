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
    new_posts = Post.objects.filter(created_at__date__gte=cache.get_or_set('last_send', datetime.date.today(), None))
    post_new_list = list(new_posts)
    cache.set('last_send', datetime.date.today(), None)
    # if len(post_new_list) != 0:
    #     for contact in Contact.objects.all():
    [send_mail(
        'Для наших подписчиков',
        'У нас новые пост(ы): {0}'.format(post_new_list),
        'x.Spirlhark.x@gmail.com',
        [contact.email],
        fail_silently=False,)for contact in Contact.objects.all() if len(post_new_list) != 0]
