from django.core.mail import send_mail
import logging


logger = logging.getLogger(__name__)


def send(user_email):
    # print("THIS IS MY FUNCTION!!!!!!!!!!!!!!!!")
    send_mail(
        'Вы подписались на рассылку',
        'Поздравляем, вы подписаны!',
        'x.spirlhark.x@gmail.com',
        [user_email],
        fail_silently=False,
    )
    # print("THIS IS MY FUNCTION!!!!!!!!!!!!!!!!")

