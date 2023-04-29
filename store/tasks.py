from celery import shared_task
from django.core.mail import send_mail
from django.http import BadHeaderError

from config import settings
from .models import Comment
from datetime import datetime, timedelta


@shared_task
def delete_disable_comments():
    time_of_now = datetime.now()
    one_week_ago = time_of_now - timedelta(seconds=4)
    comments = Comment.objects.filter(date_time_created__lt=one_week_ago)
    for comment in comments:
        try:
            send_mail('comment warning',
                      "your comment goes against out community and we can not show it in the comments",
                      settings.ADMIN_EMAIL, [comment.user.email]
                      )
        except BadHeaderError:
            pass

    comments.delete()
