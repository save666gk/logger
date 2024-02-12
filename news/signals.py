from allauth.account.signals import user_signed_up
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from .models import PostCategory, Post, Category
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .tasks import send_notifications


@receiver(user_signed_up)
def add_to_custom_group_allauth(sender, request, user, **kwargs):
    common_group = Group.objects.get(name='common')
    user.groups.add(common_group)

# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'flatpages/post_created_email.html',{
#             'text': preview,
#             'link': f'{settings.SITE_URL}//{pk}'
#         }
#
#     )
#     msq = EmailMultiAlternatives(
#         subject=title,
#         body='',
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=subscribers
#     )
#     msq.attach_alternative(html_content, 'text/html')
#     msq.send()

@receiver(m2m_changed,sender = PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.category.all()
        subscibers_emails = []

        for cat in categories:
            subscibers = cat.subscribers.all()
            subscibers_emails += [s.email for s in subscibers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscibers_emails)
        send_notifications.delay(instance.preview(), instance.pk, instance.title, subscibers_emails)

@receiver(post_save, sender=User)
def send_registration_email(sender, instance, created, **kwargs):
        if created:
            subject = 'Добро пожаловать!'
            message = f'Спасибо за регистрацию на нашем сайте {instance.username}. Добро пожаловать!'
            sender_email = 'danilka19711@yandex.ru'  # Адрес, от которого будет отправлено письмо
            receiver_email = instance.email  # Адрес получателя, в данном случае email пользователя
            send_mail(subject, message, sender_email, [receiver_email])


