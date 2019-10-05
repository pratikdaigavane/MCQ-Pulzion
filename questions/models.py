from django.db import models



# Model for Questions.

class Question(models.Model):
    problem = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    correct_option = models.CharField(max_length=1, blank=False, null=False)
    level = models.PositiveSmallIntegerField(default=1)


# Model for Scores.

class Scores(models.Model):
    name = models.TextField()
    username = models.TextField()
    event = models.TextField()
    score = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    firebase = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Scores"


# Model for Users (to be fectched form Firebase).

class auth(models.Model):
    mail = models.TextField()
    participant1 = models.TextField()
    tickedid = models.TextField()
