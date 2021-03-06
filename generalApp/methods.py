from django.http import HttpResponse
from django.db import connection
from .exchangeVO import *
from .utilities import *
from .models import *
import requests
import json
import time

# Exchange Asynchronic Notifications

@newThread
def checkTriggerNotification():
    while True:
        ExchangeVO.checkTrigger()
        connection.close()
        time.sleep(1800)

# Exchange POST Methods

def addTrigger(request):
    return Triggers.addObject(request, 1)

def addTransaction(request):
    return Transactions.addObject(request, 1)

def Prognosis(request, time, price):
    return ExchangeVO.createActualPrognosis(request, time, price, 1)

# Exchange GET Methods

def getExchangeGraph(request, time):
    return ExchangeVO.getGraphView(request, time)

def getTrigger(request, id):
    return Triggers.getObject(id)

def getTransaction(request, id):
    return Transactions.getObject(id)

def getUserTriggers(request, userID):
    return Triggers.getObjectsByParentID(userID)

def getUserTransactions(request, userID):
    return Transactions.getObjectsByParentID(userID)

def getTriggersAll(request):
    return Triggers.getAllObjects()

def getTransactionsAll(request):
    return Transactions.getAllObjects()

def getUserNotifications(request, userID):
    return Notifications.getObjectsByParentID(userID)

# Exchange PUT Methods

def putTrigger(request, id):
    return Triggers.putObject(request, id, 1)

def putTransaction(request, id):
    return Transactions.putObject(request, id, 1)

# Exchange DELETE Methods

def deleteTrigger(request, id):
    return Triggers.deleteObject(request, id, 1)

def deleteTransaction(request, id):
    return Transactions.deleteObject(request, id, 1)

def deleteNotification(request, id):
    return Notifications.deleteObject(request, id, 1)

# Forum POST Methods

def loginUser(request):
    login = jsonLoad(request)
    if login['login'] is not None and login['password'] is not None:
        users = Users.objects.all()
        for x in users:
            if x.login == login['login']:
                if checkPassHash(login['password'], x.password):
                    newSession = createSession(request, x.toDict())
                    return HttpResponse(json.dumps({ 'token': newSession }))
    return HttpResponse("Login Failed")

def logoutUser(request):
    return deleteSession(request)

def registerUser(request):
    return Users.addObject(request)

def addThread(request):
    return Threads.addObject(request, 2)

def addSubject(request, threadID):
    return Subjects.addObjectWithParent(request, threadID, 1)

def addComment(request, subjectID):
    return Comments.addObjectWithParent(request, subjectID, 1)

def addRating(request, commentID):
    return Ratings.addObjectWithParent(request, commentID, 1)

# Forum GET Methods

def getUser(request, id):
    return Users.getObject(id)

def getUsersAll(request):
    return Users.getAllObjects()

def getThreadsAll(request):
    return Threads.getAllObjects()

def getThreadSubjects(request, threadID):
    return Subjects.getObjectsByParentID(threadID)

def getSubjectComments(request, subjectID):
    return Comments.getObjectsByParentID(subjectID)

def getCommentRatings(request, commentID):
    return Ratings.getObjectsByParentID(commentID)

# Forum PUT Methods

def putUser(request, id):
    return Users.putObject(request, id, 1)


def putThread(request, id):
    return Threads.putObject(request, id, 2)


def putSubject(request, id):
    return Subjects.putObject(request, id, 1)


def putComment(request, id):
    return Comments.putObject(request, id, 1)


def putRating(request, id):
    return Ratings.putObject(request, id, 1)

# Forum DELETE Methods

def deleteUser(request, id):
    return Users.deleteObject(request, id, 1)


def deleteThread(request, id):
    return Threads.deleteObject(request, id, 2)


def deleteSubject(request, id):
    return Subjects.deleteObject(request, id, 1)


def deleteComment(request, id):
    return Comments.deleteObject(request, id, 1)


def deleteRating(request, id):
    return Ratings.deleteObject(request, id, 1)
