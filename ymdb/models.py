import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now
from django.core.files.storage import FileSystemStorage

# Create your models here.
@python_2_unicode_compatible
class GenerTag(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Название')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Collections(models.Model):
    name = models.CharField(max_length=70, unique=True, verbose_name='Название')
    BlockLabel = models.CharField(max_length=30, default='', verbose_name='Подпись для Частей')
    PartLabel = models.CharField(max_length=30, default='', verbose_name='Подпись для Элементов')
    SingleLabel = models.CharField(max_length=100, default='', verbose_name='Подпись для Самостоятельного произведения')
    AgoLabel = models.CharField(max_length=70, default='', verbose_name='Подпись для Даты')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

def update_filename(instance, filename):
    path = "ymdb/static/covers/"
    format = "%s_%s" % (instance.id, filename)
    return os.path.join(path, format)


@python_2_unicode_compatible
class ArtObject(models.Model):
    ART_STATUSES = (
        (-1, 'Без оценки'),
        (0, 'Буду смотреть'),
        (5, 'Отлично'),
        (4, 'Хорошо'),
        (3, 'Приемлемо'),
        (2, 'Плохо'),
        (1, 'Ужасно'),
    )
    ArtCover = models.URLField(verbose_name='Обложка (ссылка на изображние)', blank=True)
    # This strange ArtCoverCahed.upload_to is used beacause only one possible way to serve images in django - through django.staticfiles
    ArtCoverCahed = models.ImageField(verbose_name='Обложка (*.PNG, *.JPEG)', default='', blank=True, upload_to=update_filename)
    ExternalLink = models.URLField(verbose_name='Внешняя ссылка (описание или загрузка)', default='', blank=True)
    ArtTitle = models.CharField('Название', max_length=170)
    ArtSubTitle = models.TextField('Подзаголовок', blank=True, max_length=200)
    UserComment = models.TextField ('Ваш комментарий', blank=True)
    ArtBlocks = models.IntegerField('Томов', default=1, blank=True)
    ArtParts = models.IntegerField('Эпизодов', default=1, blank=True)
    SolidArt = models.BooleanField('Самостоятельное произведение?', default=False)
    UserRating = models.IntegerField('Ваша оценка', choices=ART_STATUSES, default=0)
    ArtGeners = models.ManyToManyField(GenerTag, blank=True, verbose_name='Жанры (Тэги)<br><span class="text-muted small">[Сtrl - несколько]</span>')
    InCollection = models.ForeignKey(Collections, blank=False, default=0, on_delete=models.CASCADE, verbose_name='Коллекция')
    ArtModified = models.DateTimeField('Добавлено', default=now)


    class Meta:
        ordering = ['-ArtModified']

class sysSettings(models.Model):
    HEAD_THEMES = (
        ('navbar-dark bg-dark', 'Тёмная'),
        ('navbar-light bg-light', 'Светлая'),
        ('navbar-light alert-secondary border-bottom border-secondary', 'Серая'),
        ('navbar-light alert-primary border-bottom border-primary', 'Голубая'),
        ('navbar-light alert-success border-bottom border-success', 'Зеленая'),
        ('navbar-light alert-warning border-bottom border-warning', 'Желатая'),
        ('navbar-light alert-danger border-bottom border-danger', 'Красная'),
    )
    theUser = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    pageStep = models.IntegerField(verbose_name='Отбражать по Х карт:', default=0)
    navTheme = models.CharField(verbose_name='Тема тулбара', choices=HEAD_THEMES, default=HEAD_THEMES[0], max_length=200)

class guestTestimonilas(models.Model):
    ArtBind = models.ForeignKey(ArtObject, on_delete=models.CASCADE)
    tsName = models.TextField(verbose_name='', blank=True, max_length=100)
    tsText = models.TextField(verbose_name='', blank=True)
    tsDate = models.DateTimeField(default=now)
    isAdmin = models.IntegerField(default=-1)

    def __str__(self):
        return self.tsName