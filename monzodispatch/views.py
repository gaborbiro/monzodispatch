from django.shortcuts import render
from django.http.response import JsonResponse
import requests
import json
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from dispatch.models import MonzoToken
from django.http.response import HttpResponse

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

def send_fcm_message(apiKey, deviceToken, notification, json):
    url = 'http://fcm.googleapis.com/fcm/send'
    headers = {"Content-Type": "application/json", "Authorization": "key=%s" % apiKey}
    payload = {"to": "chbzC9P1PTk:APA91bEQ0ZV4OqLQZOaMf4TeXCDaChzJgi3yR0g3l4HRLFYLbqF6yFcVqSHR7ugJRZrY0ulO3LHyaMSgO0z0F2ZfcOEPmOstJ8P35OO4VE9MH_QivQ_TFtk_xuIr3ETxpZXqso90V8Rt"}
    
    if notification:
        payload["notification"] = notification
    
    if json:
        payload["data"] = json
    
    r = requests.post(url, headers=headers, json=payload)
    return r.text

@csrf_exempt
def register_fcm_device(request):
    print("register_fcm_device")
    if request.method == 'POST':
        token = request.GET.get('token')
        h = hash(token)
        print("Registration request from " + str(token))
        
        monzo_tokens = MonzoToken.objects.filter(token = token)
        
        if monzo_tokens.count() > 0:
            monzo_token = monzo_tokens[0]
        else:
            monzo_token = MonzoToken(hash = h, token = token)
            monzo_token.save()
        return JsonResponse({'hash' : monzo_token.hash})
    
@csrf_exempt
def push(request, hash=None):
    if request.method == 'POST':
        apiKey = settings.FIREBASE_API_KEY
        deviceToken = MonzoToken.objects.get(hash=hash).token
        
        if deviceToken:
            print(send_fcm_message(apiKey, deviceToken, None, json.loads(request.body.decode('utf-8'))))
        pass
    return HttpResponse()
