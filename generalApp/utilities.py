from hmac import compare_digest as checkHash
from django.http import HttpResponse
from threading import Thread
import threading
import requests
import crypt
import json
import jwt

# Session / Token Methods

tokenKey = 'U0VDUkVUX1BBU1NfQ0hFQ0s#!@#SDS!#'
tokens = []

def createSession(request, userDict):
    newToken = createToken(userDict)
    tokens.append(newToken)
    return newToken

def createToken(userDict):
    return jwt.encode( { 'payload': userDict }, tokenKey, algorithm = 'HS256' ).decode('UTF-8')

def checkSession(request, privilige):
    token = tryGetTokenFromRequest(request)
    print( token )
    print( tokens )
    for currentToken in tokens:
        if token == currentToken:
            if decodeToken(currentToken)['payload']['privilige'] >= privilige:
                return True
            else:
                return False
    return False

def tryGetTokenFromRequest(request):
    try:
        return jsonLoad(request)['token']
    except:
        pass

def decodeToken(token):
    return jwt.decode( token, tokenKey, algorithms = ['HS256'] )

def checkUserPermission(modelDict, request):

    def UserIsAdmin(token):
        return decodeToken(token)['payload']['privilige'] == 3

    def UserIsModer(token):
        return decodeToken(token)['payload']['privilige'] == 2

    def checkUserChanges(modelDict, token):
        return decodeToken(token)['payload']['id'] == modelDict['user_id']

    def checkUser(modelDict, token):
        return decodeToken(token)['payload']['id'] == modelDict['id']

    def modelIsNotUser(modelDict):
        return 'user_id' in modelDict

    def modelIsUser(modelDict):
        return 'login' in modelDict

    def checkCheats(modelDict, token):
        if 'privilige' in modelDict:
            if modelDict['privilige'] != decodeToken(token)['payload']['privilige']:
                return True
            else:
                return False
        else:
            return False

    token = tryGetTokenFromRequest(request)
    if modelIsNotUser(modelDict):
        print( UserIsAdmin(token) )
        print( UserIsModer(token) )
        if UserIsAdmin(token):
            return True
        elif UserIsModer(token):
            return True
        elif checkUserChanges(modelDict, token):
            return True
        else:
            return False
    elif modelIsUser(modelDict):
        if UserIsAdmin(token):
            return True
        elif checkCheats(modelDict, token):
            return False
        elif checkUser(modelDict, token):
            return True
        else:
            return False

def deleteSession(request):
    token = jsonLoad(request)['token']
    try:
        tokens.remove(token)
        return HttpResponse("Session Has Been Deleted")
    except:
        return HttpResponse("Session Delete Error")

# Security Hash / Crypt Methods

def createPassHash(password):
    return crypt.crypt(password)

def checkPassHash(password, hashedPass):
    return checkHash(hashedPass, crypt.crypt(password, hashedPass))

# Thread Method

def newThread(function):

    def decorator(*args, **kwargs):
        thread = Thread(target = function, args = args, kwargs = kwargs)
        thread.daemon = True
        thread.start()

    return decorator

# JSON Load Method

def jsonLoad(self):
    return json.loads(self.body.decode('utf-8'))
