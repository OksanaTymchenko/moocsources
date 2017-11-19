from django.db import models
from django.contrib.auth.models import User



class Course(models.Model):
    name = models.CharField(max_length=200, null=True)
    category = models.CharField(max_length=200, null=True)
    # models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    # subcategory = models.CharField(max_length=50, null=True)
    source = models.CharField(max_length=200, null=True)
    provider = models.CharField(max_length=200, null=True)
    language = models.CharField(max_length=200, null=True)
    duration = models.CharField(max_length=200, null=True)
    duration_filter = models.CharField(max_length=200, null=True)
    start_date = models.CharField(max_length=200, null=True)
    link = models.CharField(max_length=200, null=True)
    image = models.CharField(max_length=500, null=True)
    description = models.TextField(null=True)
    video = models.CharField(max_length=200, null=True)
    # instructors = models.ForeignKey('Instructor', on_delete=models.SET_NULL, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Instructor(models.Model):
    name = models.CharField(max_length=100, null=True)
    info = models.TextField(null=True)
    course = models.ManyToManyField(Course)

    def __str__(self):              # __unicode__ on Python 2
        return self.name


class Questionnaire(models.Model):
    preferences = models.CharField(max_length= 1000, default='')
    rate = models.IntegerField(default=0)
    is_free = models.BooleanField(default= False)
    language = models.CharField(max_length=100, default='')
    duration = models.IntegerField(default=0)

class Account(models.Model):
    is_admin = models.BooleanField()
    questionaire = models.OneToOneField(Questionnaire, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

class Recommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    courses = models.CharField(max_length=200, default='')