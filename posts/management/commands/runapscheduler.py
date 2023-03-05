import datetime
import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from posts.models import Post, Category

logger = logging.getLogger(__name__)


def weekly_job():
    print("Got to the job")
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(created_at__gte=last_week)
    cats = posts.values_list('category_id__name', flat=True)
    subs = Category.objects.filter(name__in=cats).values_list('subscribers__email', flat=True)
    html = render_to_string(
        'weekly.html',
        {
            'url':settings.SITE_URL,
            'posts': posts,
        }
    )

    msg = EmailMultiAlternatives(
        subject='Your weekly digest',
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subs,
    )

    msg.attach_alternative(html,'text/html')
    msg.send()
    print("Email has been sent")



def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            weekly_job,
            trigger=CronTrigger(second="*/10"),
            # То же, что и интервал, но задача тригера таким образом более понятна django
            id="test_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'test_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            # Каждую неделю будут удаляться старые задачи, которые либо не удалось выполнить, либо уже выполнять не надо.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
