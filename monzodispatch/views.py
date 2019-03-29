import json
from datetime import datetime

import demjson
import requests
from django.conf import settings
from django.http.response import HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from monzodispatch.models import MonzoToken


@csrf_exempt
def event(request):
    body_json = request.body.decode('utf-8')
    print(body_json)
    content = demjson.decode(body_json)

    if request.method == 'POST':
        start = datetime.strptime(content['start'], "%B %d, %Y at %I:%M%p")
        end = datetime.strptime(content['end'], "%B %d, %Y at %I:%M%p")
        print("start: {}, title: {}".format(str(start), content['title']))
        token = MonzoToken.objects.latest('added').token
        data = {"event": {
            "title": content['title'],
            "start": str(start),
            "end": str(end),
            "description": content['description'],
            "where": content['where'],
            "url": content['url']}}
        send_fcm_message(token, None, data)

    return JsonResponse({'result': 'success'})


@csrf_exempt
def investments(request):
    data = {"message": "Last loaded at: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    return render(request, 'test/investments.html', data)


def form(request):
    data = {}
    if request.method == 'POST':
        device_token = request.POST.get('token').strip()
        notification_title = request.POST.get('notification_title').strip()
        notification_body = request.POST.get('notification_body').strip()
        rawData = request.POST.get('data').strip()
        notificationData = None
        if rawData:
            notificationData = demjson.decode(rawData)

        notification = None

        if notification_title or notification_body:
            notification = {"title": notification_title, "body": notification_body}

        return HttpResponse(send_fcm_message(device_token, notification, notificationData))
    else:
        try:
            data["token"] = MonzoToken.objects.latest('added').token
        except:
            pass
        return render(request, 'test/monzo_push_test.html', data)


def send_fcm_message(device_token, notification, data):
    url = 'http://fcm.googleapis.com/fcm/send'
    headers = {"Content-Type": "application/json", "Authorization": "key=%s" % settings.FIREBASE_API_KEY}
    payload = {"to": device_token}

    if notification:
        payload["notification"] = notification

    if data:
        payload["data"] = data
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
        return JsonResponse({'hash': monzo_token.hash})


@csrf_exempt
def push(request, hash=None):
    device_token = MonzoToken.objects.get(hash=hash).token

    if device_token:
        body = request.body.decode('utf-8')
        print("body: " + body)
        data = {}
        if body:
            data["monzo_data"] = json.loads(body)
        #         data["notification"] = {"title": "MonzoDispatch", "body": "Monzo pinged us"}
        print(send_fcm_message(device_token, None, data))
    return HttpResponse()
