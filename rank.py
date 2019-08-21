from questions.models import Scores
Scores.objects.all().order_by('-score')
