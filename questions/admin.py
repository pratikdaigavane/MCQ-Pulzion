from django.contrib import admin
from django.contrib.auth.models import Group

# Register your models here.
from .models import Question, Scores, auth

admin.site.site_header = 'MCQ Admin Panel'
admin.site.site_title = 'MCQ Admin Panel'


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'problem', 'level', 'correct_option')
    search_fields = ('problem',)
    list_filter = ('level',)


class ScoresAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'event', 'score', 'created')
    search_fields = ('username',)
    list_filter = ('created', 'event')
class AuthAdmin(admin.ModelAdmin):
    list_display = ('participant1', 'mail', 'tickedid')
    search_fields = ('participant1', 'mail','tickedid')




admin.site.register(Question, QuestionAdmin)
admin.site.register(Scores, ScoresAdmin)
admin.site.register(auth,AuthAdmin)
admin.site.unregister(Group)
