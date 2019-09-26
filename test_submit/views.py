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


def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

# Create your views here.


def firescore(request, dump):
    print()


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
        # ranks = Scores.objects.all().order_by('-score')[:10]
        # print("--------------------------------------------")
        # print(len(ranks))
        # print("--------------------------------------------")
        # for y in ranks:
        #     print(str(y.name) + "    " + str(y.score))

        logout(request)
        context = {
            'score': score,
            'status': 1
        }

        return JsonResponse(context)
        #return render(request, "loggedout.html", context)
    else:
        return redirect("/")
