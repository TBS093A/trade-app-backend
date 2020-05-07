from django.http import HttpResponse
from .methods import *

# Threads Start

checkTriggerNotification()

# REST Definition

def authUser(request):
    if request.method == 'POST':
        return loginUser(request)
    elif request.method == 'DELETE':
        return logoutUser(request)
    else:
        return HttpResponse('Bad Request Method')


def users(request):
    if request.method == 'GET':
        return getUsersAll(request)
    elif request.method == 'POST':
        return registerUser(request)
    else:
        return HttpResponse('Bad Request Method')


def user(request, id):
    if request.method == 'GET':
        return getUser(request, id)
    elif request.method == 'PUT':
        return putUser(request, id)
    elif request.method == 'DELETE':
        return deleteUser(request, id)
    else:
        return HttpResponse('Bad Request Method')


def threads(request):
    if request.method == 'GET':
        return getThreadsAll(request)
    elif request.method == 'POST':
        return addThread(request)
    else:
        return HttpResponse('Bad Request Method')


def thread(request, id):
    if request.method == 'PUT':
        return putThread(request, id)
    elif request.method == 'DELETE':
        return deleteThread(request, id)
    else:
        return HttpResponse('Bad Request Method')


def subjects(request, threadID):
    if request.method == 'GET':
        return getThreadSubjects(request, threadID)
    elif request.method == 'POST':
        return addSubject(request, threadID)
    else:
        return HttpResponse('Bad Request Method')


def subject(request, id):
    if request.method == 'PUT':
        return putSubject(request, id)
    elif request.method == 'DELETE':
        return deleteSubject(request, id)
    else:
        return HttpResponse('Bad Request Method')


def comments(request, subjectID):
    if request.method == 'GET':
        return getSubjectComments(request, subjectID)
    elif request.method == 'POST':
        return addComment(request, subjectID)
    else:
        return HttpResponse('Bad Request Method')


def comment(request, id):
    if request.method == 'PUT':
        return putComment(request, id)
    elif request.method == 'DELETE':
        return deleteComment(request, id)
    else:
        return HttpResponse('Bad Request Method')


def ratings(request, commentID):
    if request.method == 'GET':
        return getCommentRatings(request, commentID)
    elif request.method == 'POST':
        return addRating(request, commentID)
    else:
        return HttpResponse('Bad Request Method')

def rating(request, id):
    if request.method == 'PUT':
        return putRating(request, id)
    elif request.method == 'DELETE':
        return deleteRating(request, id)
    else:
        return HttpResponse('Bad Request Method')

def exchangeGraph(request, time):
    if request.method == 'GET':
        return getExchangeGraph(request, time)
    else:
        return HttpResponse('Bad Request Method')

def exchangePrognosis(request, price, time):
    if request.method == 'GET':
        return Prognosis(request, time, price)
    else:
        return HttpResponse('Bad Request Method')

def transactions(request, userID):
    if request.method == 'GET':
        return getUserTransactions(request, userID)
    elif request.method == 'POST':
        return addTransaction(request, userID)
    else:
        return HttpResponse('Bad Request Method')

def transaction(request, id):
    if request.method == 'GET':
        return getTransaction(request, id)
    elif request.method == 'PUT':
        return putTransaction(request, id)
    elif request.method == 'DELETE':
        return deleteTransaction(request, id)
    else:
        return HttpResponse('Bad Request Method')

def transactionsAll(request):
    if request.method == 'GET':
        return getTransactionsAll(request)
    else:
        return HttpResponse('Bad Request Method')

def triggers(request, userID):
    if request.method == 'GET':
        return getUserTriggers(request, userID)
    elif request.method == 'POST':
        return addTrigger(request, userID)
    else:
        return HttpResponse('Bad Request Method')

def trigger(request, id):
    if request.method == 'GET':
        return getTrigger(request, id)
    if request.method == 'PUT':
        return putTrigger(request, id)
    elif request.method == 'DELETE':
        return deleteTrigger(request, id)
    else:
        return HttpResponse('Bad Request Method')

def triggersAll(request):
    if request.method == 'GET':
        return getTriggersAll(request)
    else:
        return HttpResponse('Bad Request Method')

def notifications(request, userID):
    if request.method == 'GET':
        return getUserNotifications(request, userID)
    else:
        return HttpResponse('Bad Request Method')

def notification(request, id):
    if request.method == 'DELETE':
        return deleteNotification(request, id)
    else:
        return HttpResponse('Bad Request Method')
