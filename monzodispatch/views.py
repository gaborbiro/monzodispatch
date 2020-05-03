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
    url = 'https://fcm.googleapis.com/fcm/send'
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
        print("Monzo says:")
        printLongText(body)
        data = {}
        if body:
            data["monzo_data"] = json.loads(body)
        print(send_fcm_message(device_token, None, data))
    return HttpResponse()

@csrf_exempt
def test(request):
    long_text = "Material is the metaphor.\n\n\
A material metaphor is the unifying theory of a rationalized space and a system of motion.\
The material is grounded in tactile reality, inspired by the study of paper and ink, yet \
technologically advanced and open to imagination and magic.\n\
Surfaces and edges of the material provide visual cues that are grounded in reality. The \
use of familiar tactile attributes helps users quickly understand affordances. Yet the \
flexibility of the material creates new affordances that supercede those in the physical \
world, without breaking the rules of physics.\n\
The fundamentals of light, surface, and movement are key to conveying how objects move, \
interact, and exist in space and in relation to each other. Realistic lighting shows \
seams, divides space, and indicates moving parts.\n\n\
Bold, graphic, intentional.\n\n\
The foundational elements of print based design typography, grids, space, scale, color, \
and use of imagery guide visual treatments. These elements do far more than please the \
eye. They create hierarchy, meaning, and focus. Deliberate color choices, edge to edge \
imagery, large scale typography, and intentional white space create a bold and graphic \
interface that immerse the user in the experience.\n\
An emphasis on user actions makes core functionality immediately apparent and provides \
waypoints for the user.\n\n\
Motion provides meaning.\n\n\
Motion respects and reinforces the user as the prime mover. Primary user actions are \
inflection points that initiate motion, transforming the whole design.\n\
All action takes place in a single environment. Objects are presented to the user without \
breaking the continuity of experience even as they transform and reorganize.\n\
Motion is meaningful and appropriate, serving to focus attention and maintain continuity. \
Feedback is subtle yet clear. Transitions are efﬁcient yet coherent.\n\n\
3D world.\n\n\
The material environment is a 3D space, which means all objects have x, y, and z \
dimensions. The z-axis is perpendicularly aligned to the plane of the display, with the \
positive z-axis extending towards the viewer. Every sheet of material occupies a single \
position along the z-axis and has a standard 1dp thickness.\n\
On the web, the z-axis is used for layering and not for perspective. The 3D world is \
emulated by manipulating the y-axis.\n\n\
Light and shadow.\n\n\
Within the material environment, virtual lights illuminate the scene. Key lights create \
directional shadows, while ambient light creates soft shadows from all angles.\n\
Shadows in the material environment are cast by these two light sources. In Android \
development, shadows occur when light sources are blocked by sheets of material at \
various positions along the z-axis. On the web, shadows are depicted by manipulating the \
y-axis only. The following example shows the promotion with a height of 6dp.\n\n\
Resting elevation.\n\n\
All material objects, regardless of size, have a resting elevation, or default elevation \
that does not change. If an object changes elevation, it should return to its resting \
elevation as soon as possible.\n\n\
Component elevations.\n\n\
The resting elevation for a component type is consistent across apps (e.g., FAB elevation \
does not vary from 6dp in one app to 16dp in another app).\n\
Components may have different resting elevations across platforms, depending on the depth \
of the environment (e.g., TV has a greater depth than mobile or desktop).\n\n\
Responsive elevation and dynamic elevation offsets.\n\n\
Some component types have responsive elevation, meaning they change elevation in response \
to user input (e.g., normal, focused, and pressed) or system events. These elevation \
changes are consistently implemented using dynamic elevation offsets.\n\
Dynamic elevation offsets are the goal elevation that a component moves towards, relative \
to the component’s resting state. They ensure that elevation changes are consistent \
across actions and component types. For example, all components that lift on press have \
the same elevation change relative to their resting elevation.\n\
Once the input event is completed or cancelled, the component will return to its resting \
elevation.\n\n\
Avoiding elevation interference.\n\n\
Components with responsive elevations may encounter other components as they move between \
their resting elevations and dynamic elevation offsets. Because material cannot pass \
through other material, components avoid interfering with one another any number of ways, \
whether on a per component basis or using the entire app layout.\n\
On a component level, components can move or be removed before they cause interference. \
For example, a floating action button (FAB) can disappear or move off screen before a \
user picks up a promotion, or it can move if a snackbar appears.\n\
On the layout level, design your app layout to minimize opportunities for interference. \
For example, position the FAB to one side of stream of a cards so the FAB won’t interfere \
when a user tries to pick up one of cards.\n\n"

    printLongText(long_text)
    return HttpResponse()

def printLongText(long_text):
    n = 900
    tokens = [(long_text[i:i + n]) for i in range(0, len(long_text), n)]
    for token in tokens:
        print(token)
