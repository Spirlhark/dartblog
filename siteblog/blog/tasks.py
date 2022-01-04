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
    if cache.get('last_send') is None:
        cache.set('last_send', datetime.date.today(), None)
    new_posts = Post.objects.filter(created_at__date__gte=cache.get('last_send'))
    post_new_list = list(new_posts)
    cache.set('last_send', datetime.date.today(), None)
    if len(post_new_list) != 0:
        for contact in Contact.objects.all():
            send_mail(
                'Для наших подписчиков',
                'У нас новые пост(ы): {0}'.format(post_new_list),
                'x.Spirlhark.x@gmail.com',
                [contact.email],
                fail_silently=False,
            )


# @app.task
# def send_new_posts():
#     today = datetime.date.today()
#     new_posts = Post.objects.filter(created_at__date=today)
#     post_new_list = list(new_posts)
#     if len(post_new_list) != 0:
#         for user in Contact.objects.all():
#             send_mail(
#                 'Вы подписаны на рассылку',
#                 'У нас новые пост(ы): {0}'.format(post_new_list),
#                 'x.spirlhark.x@gmail.com',
#                 [user.email],
#                 fail_silently=False,
#             )
