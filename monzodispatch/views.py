from django.shortcuts import render
from django.http.response import JsonResponse
import requests
import json
from datetime import datetime
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from dispatch.models import MonzoToken
from django.http.response import HttpResponse

@csrf_exempt
def event(request):
    log = str(request.body)
    print("log: " + log)
    
    if request.method == 'POST':
        body = json.loads(request.body.decode('utf-8'))
        start = datetime.strptime(str(body['start']), "%B %d, %Y at %I:%M%p")
        print("start: {}, title: {}".format(str(start), body['title']))
    
    return JsonResponse({'log' : log})

def form(request):
    data = {}
    if request.method == 'POST':
        apiKey = settings.FIREBASE_API_KEY
        deviceToken = request.POST.get('token').strip()
        notificationTitle = request.POST.get('notification_title').strip()
        notificationBody = request.POST.get('notification_body').strip()
        
        data = None
        
        if notificationTitle or notificationBody:
            notification = {"title": notificationTitle, "body": notificationBody}
            data = {"notification": notification, "blah": "blahblah"}
        
        return HttpResponse(send_fcm_message(apiKey, deviceToken, None, data))
    else:
        try:
            data["token"] = MonzoToken.objects.latest('added').token
        except:
            pass
        return render(request, 'test/main.html', data)

def send_fcm_message(apiKey, deviceToken, notification, data):
    url = 'http://fcm.googleapis.com/fcm/send'
    headers = {"Content-Type": "application/json", "Authorization": "key=%s" % apiKey}
    payload = {"to": deviceToken}
    
    if notification:
        payload["notification"] = notification
    
    if data:
        payload["data"] = data
    print("Sending " + str(payload))
    r = requests.post(url, headers=headers, json=payload)
    return r.text

@csrf_exempt
def register_fcm_device(request):
    print("register_fcm_device")
    if request.method == 'POST':
        token = request.GET.get('token')
        h = hash(token)
        print("Registration request from " + str(token))
        
        monzo_tokens = MonzoToken.objects.filter(token=token)
        
        if monzo_tokens.count() > 0:
            monzo_token = monzo_tokens[0]
        else:
            monzo_token = MonzoToken(hash=h, token=token)
            monzo_token.save()
        return JsonResponse({'hash' : monzo_token.hash})
    
@csrf_exempt
def push(request, hash=None):
    apiKey = settings.FIREBASE_API_KEY
    deviceToken = MonzoToken.objects.get(hash=hash).token
    
    if deviceToken:
        body = request.body.decode('utf-8')
        print("body: " + body)
        data = {}
        if body:
            data["monzo_data"] = json.loads(body)
#         data["notification"] = {"title": "MonzoDispatch", "body": "Monzo pinged us"}
        print(send_fcm_message(apiKey, deviceToken, None, data))
    return HttpResponse()
