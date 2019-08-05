from datetime import datetime
from django.http import JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
import random
from questions.models import Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from config import *
import firebase_admin
from firebase_admin import credentials, firestore



cred = credentials.Certificate('./firekey.json')
if not len(firebase_admin._apps):
    firebase_admin.initialize_app(cred)
db = firestore.client()

total_questions_mcq = totalQuestions
total_questions_db = Question.objects.count()


def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def verifyTime(ctime):
    if ctime is not None and -200 <= int(ctime) - int(timestamp()) <= 200:
        return True
    return False


errdt = HttpResponse("<h2 style='color: red;'>Error : 4572724461746554696d65</h2>")


# Create your views here.


def loggedin_view(request):
    if(request.session.get('authenticate', None) == 'yes'):    
        request.session['questions'] = []
        request.session['questions'].clear()
        request.session['questions'].append(total_questions_mcq)
        for i in range(1, total_questions_mcq + 1, 1):
            request.session['questions'].append(random.randrange(1, total_questions_db + 1, 1))
        request.session['score'] = 0
        return render(request, "rules.html", {'first': request.session['questions'][1]})
    else:
        return render(request, "403.html", {})



def questions_api(request):  # if random function is used in url it always return 2
    if request.method == 'POST' and 0 < int(request.POST.get("reqid", 1)) <= totalQuestions:
        if not verifyTime(request.POST.get("time")):
            return JsonResponse({'err': 'errdt'})
        obj = Question.objects.get(id=request.session['questions'][int(request.POST.get("reqid", 1))])
        context = {
            'que': obj.problem,
            'opt1': obj.option_a,
            'opt2': obj.option_b,
            'opt3': obj.option_c,
            'opt4': obj.option_d
        }

        return JsonResponse(context)
    else:
        return HttpResponseForbidden()


def questions_view(request):
    if(request.session.get('authenticate', None) == 'yes'):       
        if not ('endtime' in request.session):
            request.session['endtime'] = int(timestamp()) + duration
            if (request.session['endtime'])%100 > 60:
                request.session['endtime']+=100
                request.session['endtime']-=60
            if (request.session['endtime'])%10000 > 6000:
                request.session['endtime']+=10000
                request.session['endtime']-=6000

        context = {
            'event': eventName,
            'total_questions_mcq': total_questions_mcq,
            'id_array': request.session['questions'],
            'dur': duration,
            'tred': tred,
            'endtime': request.session['endtime']
        }
        return render(request, "questions.html", context)
    else:
        return render(request, "403.html", {})



def loggedout_view(request):
    return render(request, "loggedout.html", {})


def register_view(request):
    
    if(request.COOKIES.get('just_cause')=='tMgaCNOgpybhQL4jZOVoViuKRsRfUyVHN9JkmBU4h7Cf6tlT33zsdSb7MShmgini'):
        request.session['authenticate'] = 'yes'
        err=""
        if request.method == "POST":
            if not verifyTime(request.POST['timestamp']):
                return errdt

            form = UserCreationForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data.get('username')
                pwd = form.cleaned_data.get('password1')
                query = db.collection("cerebro").where('email', '==', email).get()
                f = 0

                for x in query:

                    data = x.to_dict()
                    if data['email'] == email and data['ticketno'] == pwd:
                        f = 1
                        request.session['userid'] = x.id
                        name = data['name']

                if f == 1:
                    print("Firestore Successful")
                    # user = form.save()
                    user = User.objects.create_user(first_name=name, username=email, password=pwd)
                    user.save()
                    login(request, user)
                    messages.info(request, f"You are now logged in as: {name}")

                    return redirect("loggedin")
                else:
                    messages.error(request, "Invalid username or password")
                    err = "Invalid username or password"
            else:
                err = "Duplicate user (You may have already attempted the test)"
                for msg in form.error_messages:
                    messages.error(request, f"{msg}: {form.error_messages[msg]}")
        form = UserCreationForm
        context = {
            "form": form,
            "err": err
        }
        err=""
        return render(request, "login.html", context)
    else:
        return render(request, "403.html", {})



def set_cookie(response, key, value, days_expire = 7):
  if days_expire is None:
    max_age = 365 * 24 * 60 * 60  #one year
  else:
    max_age = days_expire * 24 * 60 * 60 
  expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
  response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, secure=settings.SESSION_COOKIE_SECURE or None)

def logout_request(request):
    if(request.session.get('authenticate', None) == 'yes'):
        set_cookie(response, 'just_cause', 'tMgaCNOgpybhQL4jZOVoViuKRsRfUyVHN9JkmBU4h7Cf6tlT33zsdSb7MShmgini')
        logout(request)
        messages.info(request, "Bye!")
        return redirect("register")
    else:
        return render(request, "403.html", {})

