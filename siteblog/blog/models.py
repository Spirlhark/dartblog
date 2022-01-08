from django.db import models
from django.urls import reverse

'''
Category
=========
title, slug

Tag
=========
title, slug

Post
=========
title, slug, author, content, created_at, photo, views, category, tags
'''


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категори')
    slug = models.SlugField(max_length=255, verbose_name='Url Category', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название Тэга')
    slug = models.SlugField(max_length=50, verbose_name='Url Tag', unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('tag', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = "Теги"
        ordering = ['title']


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    slug = models.SlugField(max_length=255, verbose_name='Url', unique=True)
    author = models.CharField(max_length=100, verbose_name='Автор')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Опубликовано')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, related_name='posts', verbose_name='тЭги')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = "Посты"
        ordering = ['-created_at']


class Zastavka(models.Model):
    foto = models.ImageField(upload_to='zastavka', blank=True, verbose_name='Картинка')
    nazvanie = models.CharField(max_length=50, verbose_name='Название')
    opisanie = models.CharField(max_length=150, verbose_name='Описание')

    def __str__(self):
        return self.nazvanie

    # def get_absolute_url(self):
    #     return reverse('zastavka', kwargs={'slug': self.slug})
    #
    class Meta:
        verbose_name = 'Заставка'
        verbose_name_plural = "Заставки"
        # ordering = ['nazvanie']


class Contact(models.Model):
    """Подписка на email"""
    name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(max_length=50)
    # last_send = models.DateTimeField(auto_now=True, verbose_name='Последняя рассылка')

    def __str__(self):
        return self.email


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Коментарий", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    post = models.ForeignKey(Post, verbose_name="Пост", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.post}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"