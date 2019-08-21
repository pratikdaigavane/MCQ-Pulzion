from django.db import models


# Create your models here.

class Question(models.Model):
    problem = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1, blank=False, null=False)
    level = models.PositiveSmallIntegerField(default=1)


class Scores(models.Model):
    name = models.TextField()
    username = models.TextField()
    event = models.TextField()
    score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    firebase = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Scores"
