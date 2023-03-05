from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string

from djangoProject import settings
from .models import PostCategory, Post, Category
from django.db.models.signals import m2m_changed
from djangoProject.settings import SITE_URL, EMAIL_HOST_USER
import datetime

import time


@shared_task
def hello():
    time.sleep(1)
    print("Hello, world!")


@shared_task
def send_notifications(preview, pk, title, subs):
    print("Sending new post notification")
    html = render_to_string(
        'new_post_info.html',
        {
            'text': preview,
            'url': f'{{SITE_URL}}/news/{pk}'
        }
    )
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=EMAIL_HOST_USER,
        to=subs,
    )
    msg.attach_alternative(html, 'text/html')
    # msg.send()


@shared_task
def weekly_notification():
    print("Got to the weekly job in Celery")
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    cats = posts.values_list('category_id__name', flat=True)
    subs = Category.objects.filter(name__in=cats).values_list('subscribers__email', flat=True)
    html = render_to_string(
        'weekly.html',
        {
            'url': settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your weekly digest',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subs,
    )

    msg.attach_alternative(html, 'text/html')
    # msg.send()
    print("Email has been sent")
