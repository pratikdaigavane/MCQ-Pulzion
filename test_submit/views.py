from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import datetime
from func_timeout import func_timeout, FunctionTimedOut
from questions.models import Question, Scores
import json
from firebase_admin import credentials, firestore
from config import *
from django.contrib.auth import logout

cred = credentials.Certificate('./firekey.json')
db = firestore.client()

# Get current timestamp.

def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Gets the answers of user, checks with actual answers from Database and
# calculates the score as per the marking scheme defined in config.py file.

def submit_data(request):
    ansdict = json.loads(str(request.POST['answers']))
    print(str(ansdict))
    if request.user.is_authenticated:
        for i in ansdict:
            if Question.objects.get(id=i).correct_option.upper() == ansdict[i].upper():
                request.session['score'] += marksCorrect
                print('id:'+i+':'+Question.objects.get(id=i).correct_option.upper())
            else:
                request.session['score'] -= marksIncorrect

        fb=0
        print(request.session['score'])
        score = request.session['score']
        Scores.objects.create(name=request.session['name'], username=request.user.username,
                              event=eventName, score=score, firebase=fb)

        logout(request)
        context = {
            'score': score,
            'status': 1
        }

        return JsonResponse(context)
    else:
        return redirect("/")
