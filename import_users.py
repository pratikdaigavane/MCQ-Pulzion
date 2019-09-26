import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mcq.settings")
import django
django.setup()
from questions.models import auth

from firebase_admin import credentials, firestore
import firebase_admin

cred = credentials.Certificate("pascregistrationappdemo-firebase-adminsdk-db0o6-f51fd3003b.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
docs = db.collection('Recode_It').stream()
print(docs)
count = 0
for doc in docs:
    try:
        data = doc.to_dict()
        mail = data['mail']
        tickedid = data['id']
        participant1 = data['participant1']
        try:
            listing = auth.objects.get(mail=mail)
            print("already added " + data['mail'])
        except auth.DoesNotExist:
            listing = None
            print(mail)
            auth.objects.create(
            mail=mail, participant1=participant1, tickedid=tickedid)
            count+=1
    except:
        print(doc.id + " not imported")
print("added "+ str(count)+" entries")


    # from urllib.request import urlopen as uReq
