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
from func_timeout import func_timeout, FunctionTimedOut
from questions.models import auth

cred = credentials.Certificate('./firekey.json')
if not len(firebase_admin._apps):
    firebase_admin.initialize_app(cred, options={'httpTimeout': 3})
db = firestore.client()

total_questions_mcq = totalQuestions
total_questions_db = Question.objects.count()


def loginquery(email, pwd, request):
    # request.session['userid'] = x.id
    # request.session['name'] = data['name']
    # name = data['name']

    check = auth.objects.filter(mail=email, tickedid=pwd)
    length = check.count()
    if length != 0:
        request.session['name'] = check[0].participant1
        print("validated " + check[0].mail)
        name = check[0].participant1
        return 1
    return 0


def timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def verifyTime(ctime):
    if ctime is not None and -200 <= int(ctime) - int(timestamp()) <= 200:
        return True
    return False


errdt = HttpResponse(
    "<h2 style='color: red;'>Error : 4572724461746554696d65</h2>")


# Create your views here.

def loggedin_view(request):
    request.session['questions'] = []
    request.session['questions'].clear()
    request.session['questions'].append(-1)
    while True:
        r = random.randrange(1, total_questions_db + 1, 1)
        if r not in request.session['questions']:
            request.session['questions'].append(r)
        if len(request.session['questions']) == total_questions_mcq+1:
            break

    request.session['questions'][0] = total_questions_mcq
    request.session['score'] = 0
    print(request.session['questions'])
    print(len(request.session['questions']))


def questions_api(request):  # if random function is used in url it always return 2
    if request.method == 'POST' and 0 < int(request.POST.get("reqid", 1)) <= totalQuestions:
        if not verifyTime(request.POST.get("time")):
            return JsonResponse({'err': 'errdt'})
        obj = Question.objects.get(
            id=request.session['questions'][int(request.POST.get("reqid", 1))])
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
    if (request.session.get('authenticate', None) == 'yes'):
        if not ('endtime' in request.session):
            request.session['endtime'] = int(timestamp()) + duration
            if (request.session['endtime']) % 100 > 60:
                request.session['endtime'] += 100
                request.session['endtime'] -= 60
            if (request.session['endtime']) % 10000 > 6000:
                request.session['endtime'] += 10000
                request.session['endtime'] -= 6000

        context = {
            'event': eventName,
            'total_questions_mcq': total_questions_mcq,
            'id_array': request.session['questions'],
            'dur': duration,
            'tred': tred,
            'endtime': request.session['endtime'],
            'userName': request.session['name'],
            'ideHost': ideHost
        }
        return render(request, "questions.html", context)
    else:
        return render(request, "403.html", {})


def loggedout_view(request):
    return render(request, "loggedout.html", {})


def register_view(request):
    if (request.COOKIES.get('just_cause') == 'tMgaCNOgpybhQL4jZOVoViuKRsRfUyVHN9JkmBU4h7Cf6tlT33zsdSb7MShmgini' or not (
            useElectron)):
        request.session['authenticate'] = 'yes'
        err = ""
        if request.method == "POST":
            if not verifyTime(request.POST['timestamp']):
                return errdt
                print("dterr")

            form = UserCreationForm(request.POST)

            if form.is_valid():
                email = form.cleaned_data.get('username')
                pwd = form.cleaned_data.get('password1')
                f = -1
                try:
                    f = func_timeout(
                        15, loginquery, args=(email, pwd, request))
                except FunctionTimedOut:
                    print("Error E-55692 = Firebase Error")
                    err = "Error E-55692. Contact PASC volunteer or try again"
                if f == 1:
                    # user = form.save()
                    user = User.objects.create_user(
                        first_name=request.session['name'], username=email, password=pwd)
                    user.save()
                    login(request, user)
                    # messages.info(request, f"You are now logged in as: {name}")
                    print("Auth success")
                    loggedin_view(request)
                    return JsonResponse({'status': 1})
                elif f == 0:
                    err = "Invalid username or password"
                    print(err)
                    return JsonResponse({'status': 0, 'err': err})
                # except:
                #     print("Error E-55692 = Firebase Error")
                #     err = "Error E-55692. Contact PASC volunteer or try again"

            else:
                if "username already exists" in str(form.errors):
                    err = "Duplicate user (You may have already attempted the test)"
                else:
                    err = "Invalid data entered"
                print(form.errors)
                # err = str(form.errors)
                return JsonResponse({'status': 0, 'err': err})

        form = UserCreationForm
        context = {
            "form": form,
            "err": err,
            'eventName': eventName
        }
        err = ""
        return render(request, "login.html", context)
    else:
        return render(request, "403.html", {})


def set_cookie(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60  # one year
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                         "%a, %d-%b-%Y %H:%M:%S GMT")
    response.set_cookie(key, value, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN,
                        secure=settings.SESSION_COOKIE_SECURE or None)


def logout_request(request):
    if (request.session.get('authenticate', None) == 'yes'):
        set_cookie(response, 'just_cause',
                   'tMgaCNOgpybhQL4jZOVoViuKRsRfUyVHN9JkmBU4h7Cf6tlT33zsdSb7MShmgini')
        logout(request)
        messages.info(request, "Bye!")
        return redirect("register")
    else:
        return render(request, "403.html", {})
