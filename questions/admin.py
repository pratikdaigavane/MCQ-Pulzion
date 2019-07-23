from django.contrib import admin

# Register your models here.
from .models import Question, Scores

admin.site.register(Question)
admin.site.register(Scores)