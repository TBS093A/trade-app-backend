from django.http import HttpResponse
from .models import Lobby
import json

# REST Definition

def chatIndex(request):
    if request.method == 'GET':
        return HttpResponse(Lobby.allObjectsDict(Lobby))
    if request.method == 'POST':
        Lobby.save(json.load(request))

def chatConnect(request, roomName):
    if request.method == 'GET':
        return HttpResponse(f'connect to {roomName}')
    if request.method == 'DELETE':
        return HttpResponse('leave the chatroom')
    