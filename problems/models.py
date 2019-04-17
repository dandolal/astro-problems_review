from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils import timezone


class Problem(models.Model):
    title = models.CharField(default='', max_length=50, blank=True)
    text = models.TextField(default='')  # unique=True)
    complexity = models.IntegerField(default=0)
    solution = models.TextField(default='')
    year = models.IntegerField(default=0)
    max_level = models.IntegerField(default=1,
                                    validators=[MaxValueValidator(11), MinValueValidator(1)])
    min_level = models.IntegerField(default=1,
                                    validators=[MaxValueValidator(11), MinValueValidator(1)])
    is_solved = models.BooleanField(default=False)
    liked_users = models.ManyToManyField(User, blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return '{} ({})'.format(str(self.title), str(self.id))


DEFAULT_IMAGE = '/problems/static/problems/placeholder.jpg'


class Author(models.Model):
    problems = models.ManyToManyField(Problem, blank=True)
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='', blank=True)
    photo = models.ImageField(default=DEFAULT_IMAGE, blank=True)

    def __str__(self):
        return str(self.name)


class Theme(models.Model):
    problems = models.ManyToManyField(Problem, blank=True)
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return '{} ({})'.format(str(self.name), str(self.id))


class Event(models.Model):
    problems = models.ManyToManyField(Problem, blank=True)
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='', blank=True)

    def __str__(self):
        return '{}'.format(str(self.name))


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=50, default='')
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(default=timezone.now)
    text = models.TextField(default='')

    def __str__(self):
        return '{} {}'.format(self.author.username, str(self.date))
