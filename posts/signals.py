from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .tasks import send_notifications

from .models import PostCategory


# @receiver(post_save, sender=Post)  # Decorator to link to signal
# def notify_client_news(sender, instance, **kwargs):
#     send_mail(
#         subject=f"{instance.title[:20]}...",
#         message=f"{instance.text[:50]}",
#         from_email="@.is",
#         recipient_list=["@gmail.com"]
#     )


# Another way
# post_save.connect(notify_client_news, sender=Post)


# @receiver(post_delete, sender=Post)
# def notify_deleted_post(sender, instance, **kwargs):
#     send_mail(
#         subject=f"Someone deleted: {instance.title[:20]}...",
#         message=f"POST DELETED: {instance.text[:50]}",
#         from_email="@.is",
#         recipient_list=["@gmail.com"]
#     )


@receiver(m2m_changed, sender=PostCategory)
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        print("GOT TO THE SIGNAL")

        category = instance.category_id.all()
        subs = []
        for cat in category:
            subs += cat.subscribers.all()
        subs = [s.email for s in subs]
        print(category)
        print(subs)

        send_notifications(instance.preview(), instance.pk, instance.title, subs)
