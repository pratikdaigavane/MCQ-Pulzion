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

def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Create your views here.


def firescore(request, dump):
    db.collection("cerebro").document(request.session['userid']).update({'score': request.session['score']})


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

        try:
            func_timeout(7, firescore, args=(request, 0))
            fb = 1
        except FunctionTimedOut:
            fb = 0

        print(request.session['score'])
        score = request.session['score']
        Scores.objects.create(username=request.user.username, event=eventName, score=score, firebase=fb)
        logout(request)
        context = {
            'score': score
        }

        return render(request, "loggedout.html", context)
    else:
        return redirect("/")
        
