from celery import shared_task
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, PostCategory
from django.conf import settings
from django.utils import timezone

@shared_task
def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'flatpages/post_created_email.html',{
            'text': preview,
            'link': f'{settings.SITE_URL}//{pk}'
        }

    )
    msq = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    msq.attach_alternative(html_content, 'text/html')
    msq.send()

@shared_task
def get_new_articles_for_subscribers(self):
    week_ago = timezone.now() - timezone.timedelta(days=7)
    new_articles_for_subscribers = {}
    subscribers = PostCategory()

    for subscriber in subscribers.objects.all():
        new_posts = Post.objects.filter(category=self, dateCreation__gte=week_ago)
        new_articles_for_subscribers[subscriber.username] = list(
            new_posts)

        article_data = [(post.title, post.id) for post in new_articles_for_subscribers[subscriber.username]]
        # Генерируем сообщение, используя HTML-шаблон и список кортежей article_data
        message = render_to_string('flatpages/new_articles_notification.html',
                                   {'subscriber': subscriber, 'article_data': article_data})

        # Устанавливаем тему электронного письма
        subject = 'Список новых статей'

        # Устанавливаем отправителя
        from_email = 'danilka19711@yandex.ru'  # Укажите свой адрес электронной почты

        # Получаем адрес электронной почты получателя
        subscriber_email = subscriber.email

        # Отправляем электронное письмо
        send_mail(
            subject,
            message,
            from_email,
            [subscriber_email],
            html_message=message,
        )