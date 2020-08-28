from django.db import models
from django.http import HttpResponse
from django.db.models import Avg
from datetime import datetime
from .utilities import *


class ObjectAbstract(models.Model):

    @classmethod
    def addObject(self, request, parentID, privilige):
        if self.modelIsUser(self) or checkSession(request, privilige):
            object = jsonLoad(request)
            if self.modelIsUser(self):
                object['privilige'] = 1
                object['password'] = createPassHash(object['password'])
            if self.checkUniqueValues(self, parentID, object):
                 return self.saveObject(self, parentID, object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")

    def modelIsUser(model):
        return model == Users

    def checkUniqueValues(model, parentID, objectDict):
        objectsAll = model.allObjectsDict(model)
        for x in objectsAll:
            if model == Users:
                if x['login'].upper() == objectDict['login'].upper():
                    return False
            elif model == Threads:
                if x['name'].upper() == objectDict['name'].upper():
                    return False
            elif model == Ratings:
                if int(x['user_id']) == int(objectDict['user_id']) and int(x['comment_id']) == parentID:
                    return False
        return True

    @classmethod
    def allObjectsDict(model):
        objectAll = model.objects.all()
        list = []
        for x in objectAll:
            list.append(x.toDict())
        return list

    def modelIsNotUser(model):
        return model != Users

    def saveObject(model, parentID, objectDict):
        newObject = model()
        newObject.fromDict(objectDict)
        if model.modelHaveParent(model):
            newObject.setParentID(parentID)
        if model.modelIsTrigger(model):
            newObject.setActualTime()
        newObject.save()
        if model.modelIsSubject(model) and model.newCommentInNewSubject(objectDict):
            newComment = Comments(subject = newObject)
            newComment.fromDict(objectDict['comment'])
            newComment.save()
            return HttpResponse(f"{model.__name__}/{Comments}: Add new Objects: {newObject.toDict()} and {newComment.toDict()}")
        return HttpResponse(f"{model.__name__}: Add new Object: {newObject.toDict()}")

    def modelHaveParent(model):
        return model != Threads and model != Users

    def modelIsTrigger(model):
        return model == Triggers

    def modelIsSubject(model):
        return model == Subjects

    def newCommentInNewSubject(objectDict):
        return 'comment' in objectDict

    @classmethod
    def getObject(self, request, objectID, privilige):
        return self.getObjectNormal(self, objectID)

    def getObjectNormal(model, objectID):
        object = model.objects.get(pk = objectID).toDict()
        return HttpResponse(json.dumps(object))

    @classmethod
    def getAllObjects(self, request, privilige):
        objectsAll = self.allObjectsDict(self)
        return HttpResponse(json.dumps(objectsAll))

    @classmethod
    def getObjectsByParentID(self, request, parentID, privilige):
        if self.modelHaveParent(self):
            return HttpResponse(self.getAllByParentID(parentID))
        return HttpResponse("No Permission")

    @classmethod
    def putObject(self, request, objectID, privilige):
        if checkSession(request, privilige):
            object = jsonLoad(request)
            return self.updateObject(self, request, object, objectID)
        else:
            return HttpResponse("No Permission")

    def updateObject(model, request, objectDict, objectID):
        objectOld = model.objects.get(pk = objectID)
        if model.modelIsUser(model):
            if checkPassHash(objectDict['passwordOld'], objectOld.password):
                if 'passwordNew' in objectDict.keys():
                    objectDict['password'] = createPassHash(objectDict['passwordNew'])
            else:
                return HttpResponse('Bad Password')
        objectOld.fromDict(objectDict)
        if checkUserPermission(objectOld.toDict(), request):
            objectOld.save()
            return HttpResponse(f"{model.__name__}: {objectOld.toDict()} has been updated")
        else:
            return HttpResponse("No Permission")

    @classmethod
    def deleteObject(self, request, objectID, privilige):
        if checkSession(request, privilige):
            objectDel = self.objects.get(pk = objectID)
            if checkUserPermission(objectDel.toDict(), request):
                if self.modelIsUser(self):
                    if checkPassHash(objectDict['password'], objectDel.password):
                        pass
                    else:
                        return HttpResponse("Bad Password")
                objectDel.delete()
                return HttpResponse(f"{self.__name__}: {objectDel} has been deleted")
            else:
                return HttpResponse("No Permission")
        else:
            return HttpResponse("No Permission")

    class Meta:
        abstract = True


class Users(ObjectAbstract):
    login       = models.CharField(max_length=30)
    password    = models.CharField(max_length=200)
    email       = models.EmailField(max_length=50)
    avatar      = models.CharField(max_length=255, default='none')
    privilige   = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id} {self.login}"

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "login": self.login,
                "avatar": self.avatar,
                "email": self.email,
                "privilige": self.privilige}

    def addObject(self, request, parentID, privilige):
        newUser = jsonLoad(request)
        newUser['privilige'] = 1
        newUser['password'] = createPassHash(object['password'])
        if self.validateUnique(self, parentID, newUser):
                return self.saveObject(self, parentID, newUser)
        else:
            return HttpResponse("User Is Already Exist")

    def __validateUnique(self, parentID, userDict):
        usersAll = self.allObjectsDict(User)
        for user in usersAll:
            if user['login'].upper() == userDict['login'].upper():
                return False
        return True

    def __saveObject(model, parentID, objectDict):
        newUser = User()
        newUser.fromDict(objectDict)
        newUser.save()
        return HttpResponse(f"Add new User: {newUser.toDict()}")


class Threads(ObjectAbstract):
    name        = models.CharField(max_length=30)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)

    def __str__(self):
        return self.name

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "name": self.name,
                "user_id": self.user.id,
                "moderator": self.user.login,
                "moderator_avatar": self.user.avatar,
                "moderator_privilige": self.user.privilige}


class Subjects(ObjectAbstract):
    name        = models.CharField(max_length=30)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    thread      = models.ForeignKey(Threads, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.id} {self.name}"

    def setParentID(self, parentID):
        self.__dict__.update({ "thread_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objects.filter(thread_id = parentID)]
        return json.dumps(list)

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "name": self.name,
                "user_id": self.user.id,
                "author": self.user.login,
                "author_avatar": self.user.avatar,
                "author_privilige": self.user.privilige,
                "thread_id": self.thread.id,
                "thread_name": self.thread.name}


class Comments(ObjectAbstract):
    text        = models.CharField(max_length=1000)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    subject     = models.ForeignKey(Subjects, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.subject}"

    def setParentID(self, parentID):
        self.__dict__.update({ "subject_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objects.filter(subject_id = parentID)]
        return json.dumps(list)

    def commentSVG(self):
        return

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "text": self.text,
                "ratings_avg": Ratings.objects.filter(comment_id = self.id).aggregate(Avg('value')),
                "user_id": self.user.id,
                "author": self.user.login,
                "author_avatar": self.user.avatar,
                "author_privilige": self.user.privilige,
                "subject_id": self.subject.id,
                "subject_name": self.subject.name}


class Ratings(ObjectAbstract):
    value       = models.IntegerField()
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    comment     = models.ForeignKey(Comments, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user}, value: {self.value} -> comment in: {self.comment.subject}"

    def setParentID(self, parentID):
        self.__dict__.update({ "comment_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objects.filter(comment_id = parentID)]
        return json.dumps(list)

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "value": self.value,
                "user_id": self.user.id,
                "author": self.user.login,
                "author_avatar": self.user.avatar,
                "comment_id": self.comment.id,
                "subject": self.comment.subject.name}


class Transactions(ObjectAbstract):
    price               = models.FloatField(default=255)
    price_forecast      = models.FloatField(default=255)
    currency            = models.CharField(max_length=255)
    date_of_transaction = models.DateTimeField('date of transaction')
    course_on_payment   = models.FloatField(default=255)
    user                = models.ForeignKey(Users, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.login}, cash: {self.price}, prognosis: {self.price_forecast}"

    def setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objects.filter(user_id = parentID)]
        return json.dumps(list)

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "price": self.price,
                "currency": self.currency,
                "date_of_transaction": self.date_of_transaction,
                "course_on_payment": self.course_on_payment,
                "user_id": self.user.id,
                "author": self.user.login,
                "exchange_id": self.exchange.id}


class Triggers(ObjectAbstract):
    course_values_for_trigger   = models.FloatField(default=255)
    date_of_trigger             = models.CharField(max_length=255)
    status                      = models.IntegerField(default=1)
    user                        = models.ForeignKey(Users, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.user.login}, trigger value: {self.course_values_for_trigger}, date: {self.date_of_trigger}"

    def setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objects.filter(user_id = parentID)]
        return json.dumps(list)

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "course_values_for_trigger": self.course_values_for_trigger,
                "date_of_trigger": self.date_of_trigger,
                "status": self.status,
                "user_id": self.user.id,
                "author": self.user.login,}

    def setActualTime(self):
        self.date_of_trigger = str(datetime.now().strftime("%Y-%d-%m %H:%M"))


class Notifications(ObjectAbstract):
    message     = models.CharField(max_length=255)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)

    def __str__(self):
        return f"Message: {self.message}, for User: {self.user.login}"

    def setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    @classmethod
    def getAllByParentID(self, parentID):
        return json.dumps(list(self.objects.filter(user_id = parentID).values()))

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "message": self.message,
                "user_id": self.user.id}
