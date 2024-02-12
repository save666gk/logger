from django.core.mail import send_mail
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Sum
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.core.mail import send_mail
from django.template.loader import render_to_string

class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

class Category(models.Model):
    name = models.CharField(max_length=256, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def get_new_articles_for_subscribers(self):
        week_ago = timezone.now() - timezone.timedelta(days=7)
        new_articles_for_subscribers = {}

        # for subscriber in self.subscribers.all():
        #     new_posts = Post.objects.filter(category=self, dateCreation__gte=week_ago)
        #     new_articles_for_subscribers[subscriber.username] = list(
        #         new_posts)  # Сохраняем новые статьи для текущего подписчика
        #
        #     article_data = [(post.title, post.id) for post in new_articles_for_subscribers[subscriber.username]]
        #     # Генерируем сообщение, используя HTML-шаблон и список кортежей article_data
        #     message = render_to_string('flatpages/new_articles_notification.html',
        #                                {'subscriber': subscriber, 'article_data': article_data})
        #
        #     # Устанавливаем тему электронного письма
        #     subject = 'Список новых статей'
        #
        #     # Устанавливаем отправителя
        #     from_email = 'danilka19711@yandex.ru'  # Укажите свой адрес электронной почты
        #
        #     # Получаем адрес электронной почты получателя
        #     subscriber_email = subscriber.email
        #
        #     # Отправляем электронное письмо
        #     send_mail(
        #         subject,
        #         message,
        #         from_email,
        #         [subscriber_email],
        #         html_message=message,
        #     )

    def __str__(self):
        return self.name
class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    ARTICLE = 'AR'
    NEWS = 'NW'
    Kinds = (
        (NEWS, 'Статья'),
        (ARTICLE, 'Новость')
    )
    kindCategory = models.CharField(max_length=2, choices=Kinds, default=ARTICLE)
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=256, verbose_name='Наименование')
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/post/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        from django.core.cache import cache
        cache.delete(f'post-{self.pk}')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()





