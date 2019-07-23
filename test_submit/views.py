from django.shortcuts import render, redirect
from questions.models import Question, Scores
import json
from firebase_admin import credentials, firestore
from config import *
from django.contrib.auth import logout

cred = credentials.Certificate('./firekey.json')
db = firestore.client()


# Create your views here.


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

        db.collection("cerebro").document(request.session['userid']).update({'score': request.session['score']})
        print(request.session['score'])
        score = request.session['score']
        Scores.objects.create(username=request.user.username, event=eventName, score=score)
        logout(request)
        context = {
            'score': score
        }

        return render(request, "loggedout.html", context)
    else:
        return redirect("/")
