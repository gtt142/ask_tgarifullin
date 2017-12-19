from __future__ import unicode_literals
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import Count

# Create your models here.

class MyUserManager(UserManager):
    def get_top_N(self,N):
        return self.order_by('-rating')[0:N]



class User(AbstractUser):
    upload = models.ImageField(default='static/img/ava.png', upload_to='%Y/%m/%d/', verbose_name=u"Аватар")
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг")
    objects = MyUserManager()


class QuestionManager(models.Manager):
    def top_questions(self):
        return self.filter(is_active=True).order_by('-status__likesNum')
    def new_questions(self):
        return self.filter(is_active=True).order_by('-create_date')
    def questions_tag(self, tag_word):
        return self.filter(is_active=True, tags__title__iexact=tag_word).order_by('-status__likesNum')
    def set_like(self, q_id, d_like):
        obj = Question.objects.get(id=q_id)
        stat = obj.status
        oldLikesNum = stat.likesNum
        stat.likesNum = oldLikesNum + d_like
        stat.save()


class Category(models.Model):
    title = models.CharField(max_length=120, unique=True, verbose_name=u"Заголовок категории")

    def __str__(self):
        return self.title


class TagManager(models.Manager):
    def get_top_N(self,N):
        return self.values('title').annotate(num_questions=Count('question')).order_by('-num_questions')[0:N]


class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True, verbose_name=u"Заголовок тега")
    objects = TagManager()

    def __str__(self):
        return self.title


class Status(models.Model):
    viewsNum = models.IntegerField(default=0, verbose_name=u"Количество просмотров")
    likesNum = models.IntegerField(default=0, verbose_name=u"Количество лайков")


class Question(models.Model):
    author = models.ForeignKey(User)
    title = models.CharField(max_length=120, verbose_name=u"Заголовок вопроса")
    text = models.TextField(verbose_name=u"Полное описание вопроса")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания вопроса")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность вопроса")
    tags = models.ManyToManyField(Tag, blank=True)
    category = models.ForeignKey(Category, blank=True)
    status = models.OneToOneField(Status)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']


class AnswerManager(models.Manager):
    def set_like(self, a_id, d_like):
        obj = Answer.objects.get(id=a_id)
        oldRating = obj.rating
        obj.rating = oldRating + d_like
        obj.save()


class Answer(models.Model):
    author = models.ForeignKey(User)
    text = models.TextField(verbose_name=u"Текст ответа")
    create_date = models.DateTimeField(default=datetime.now, verbose_name=u"Время создания ответа")
    is_active = models.BooleanField(default=True, verbose_name=u"Доступность ответа")
    is_correct = models.BooleanField(default=False, verbose_name=u"Правильность ответа")
    question = models.ForeignKey(Question)
    rating = models.IntegerField(default=0, verbose_name=u"Рейтинг")
    objects = AnswerManager()
