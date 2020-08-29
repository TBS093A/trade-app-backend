from django.db import models
from django.http import HttpResponse
from django.db.models import Avg
from datetime import datetime
from .utilities import *
from .AbstractCRUD import AbstractCRUD


class ObjectAbstract(models.Model):

    @classmethod
    def addObject(self, request, parentID, privilige):
        if checkSession(request, privilige):
            object = jsonLoad(request)
            if self.__checkUniqueValues(self, parentID, object):
                 return self.__saveObject(self, parentID, object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")

    def __checkUniqueValues(model, parentID, objectDict):
        objectsAll = model.__allObjectsDict(model)
        for x in objectsAll:
            if model == Ratings:
                if int(x['user_id']) == int(objectDict['user_id']) and int(x['comment_id']) == parentID:
                    return False
        return True

    def __saveObject(model, parentID, objectDict):
        newObject = model()
        newObject.fromDict(objectDict)
        if model.modelHaveParent(model):
            newObject.setParentID(parentID)
        if model.modelIsTrigger(model):
            newObject.setActualTime()
        newObject.save()
        return HttpResponse(f"{model.__name__}: Add new Object: {newObject.toDict()}")

    @classmethod
    def __allObjectsDict(model):
        objectAll = model.objects.all()
        list = []
        for x in objectAll:
            list.append(x.toDict())
        return list

    def modelIsNotUser(model):
        return model != Users

    def modelHaveParent(model):
        return model != Threads and model != Users

    def modelIsTrigger(model):
        return model == Triggers

    def modelIsSubject(model):
        return model == Subjects

    def newCommentInNewSubject(objectDict):
        return 'comment' in objectDict

    @classmethod
    def getObject(self, request, objectID, privilige): # request, privilige is unnecessary
        return self.__getObjectNormal(self, objectID)

    def __getObjectNormal(model, objectID):
        object = model.objects.get(pk = objectID).toDict()
        return HttpResponse(json.dumps(object))

    @classmethod
    def getAllObjects(self, request, privilige):
        objectsAll = self.__allObjectsDict(self)
        return HttpResponse(json.dumps(objectsAll))

    @classmethod
    def getObjectsByParentID(self, request, parentID, privilige):
        if self.modelHaveParent(self):
            return HttpResponse(self.getAllByParentID(parentID))
        return HttpResponse("No Permission")

    # @classmethod
    # def putObject(self, request, objectID, privilige):
    #     if checkSession(request, privilige):
    #         object = jsonLoad(request)
    #         return self.updateObject(self, request, object, objectID)
    #     else:
    #         return HttpResponse("No Permission")

    @classmethod
    def putObject(self, request, objectID, privilige):
        object = jsonLoad(request) 
        if checkSession(request, privilige) and checkUserPermission(object, request)
            return self.updateObject(request, object, objectID)
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
    def deleteObject(model, request, objectID, privilige):
        objectDel = model.objects.get(pk = objectID)
        if checkSession(request, privilige) and checkUserPermission(objectDel.toDict(), request):
            objectDel.delete()
            return HttpResponse(f"{model.__name__}: {objectDel} has been deleted")
        else:
            return HttpResponse("No Permission")

    class Meta:
        abstract = True


class Users(AbstractCRUD):
    login       = models.CharField(max_length=30)
    password    = models.CharField(max_length=200)
    email       = models.EmailField(max_length=50)
    avatar      = models.CharField(max_length=255, default='none')
    privilige   = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.id} {self.login}"

    def toDict(self):
        return {"id": self.id,
                "login": self.login,
                "avatar": self.avatar,
                "email": self.email,
                "privilige": self.privilige}

    # Object Factory for abstract

    def objectFactory():
        return Users()

    # Get One User

    def __getObjectNormal(objectID):
        oneUser = Users.objects.get(pk = objectID).toDict()
        return HttpResponse(json.dumps(oneUser))

    # Create User

    @classmethod
    def addObject(request, privilige):
        newUser = jsonLoad(request)
        newUser['privilige'] = 1
        newUser['password'] = createPassHash(object['password'])
        if self.__validateUnique(newUser):
                return self.__saveObject(newUser)
        else:
            return HttpResponse("User Is Already Exist")

    def __validateUnique(userDict):
        usersAll = self.__allObjectsDict(User)
        for user in usersAll:
            if user['login'].upper() == userDict['login'].upper():
                return False
        return True

    def __saveObject(objectDict):
        newUser = Users()
        newUser.fromDict(objectDict)
        newUser.save()
        return HttpResponse(f"Add new User: {newUser.toDict()}")

    # Update User

    def updateObject(self, userDict, objectID):
        putUser = Users.objects.get(pk = objectID)
        if checkPassHash(userDict['passwordOld'], putUser.password):
            if 'passwordNew' in userDict.keys():
                userDict['password'] = createPassHash(objectDict['passwordNew'])
        else:
            return HttpResponse('Bad Password')
        putUser.fromDict(userDict)
        putUser.save()
        return HttpResponse(f"User: {putUser.toDict()} has been updated")

    # Delete User

    @classmethod
    def deleteObject(request, objectID, privilige):
        objectDel = Users.objects.get(pk = objectID)
        if checkSession(request, privilige) and checkUserPermission(objectDel.toDict(), request):
            if checkPassHash(objectDict['password'], objectDel.password):
                pass
            else:
                return HttpResponse("Bad Password")
            objectDel.delete()
            return HttpResponse(f"User: {objectDel.toDict()} has been deleted")
        else:
            return HttpResponse("No Permission")


class Threads(AbstractCRUD):
    name        = models.CharField(max_length=30)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)

    parent_id_field = 'user_id'

    def __str__(self):
        return self.name

    def toDict(self):
        return {"id": self.id,
                "name": self.name,
                "user_id": self.user.id,
                "moderator": self.user.login,
                "moderator_avatar": self.user.avatar,
                "moderator_privilige": self.user.privilige}

    # Object Factory for abstract

    def objectFactory():
        return Threads()

    # Create Thread (validation)

    def _validateUnique(self, objectDict):
        objectsAll = Threads.__allObjectsDict(model)
        for x in objectsAll:
            if x['name'].upper() == objectDict['name'].upper():
                return False
        return True


class Subjects(AbstractCRUD):
    name        = models.CharField(max_length=30)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    thread      = models.ForeignKey(Threads, on_delete = models.CASCADE)

    parent_id_field = 'thread_id'

    def __str__(self):
        return f"{self.id} {self.name}"

    def setParentID(self, parentID):
        self.__dict__.update({ "thread_id": parentID })

    def toDict(self):
        return {"id": self.id,
                "name": self.name,
                "user_id": self.user.id,
                "author": self.user.login,
                "author_avatar": self.user.avatar,
                "author_privilige": self.user.privilige,
                "thread_id": self.thread.id,
                "thread_name": self.thread.name}
    
    # Object Factory for abstract

    def objectFactory():
        return Subjects()

    # Create Subject ( create new subject + comment ones )

    def _createFirstComment(newSubject, objectDict):
        newComment = Comments(subject = newSubject)
        newComment.fromDict(objectDict['comment'])
        newComment.save()

    # Update Subject

    # Delete Subject


class Comments(AbstractCRUD):
    text        = models.CharField(max_length=1000)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    subject     = models.ForeignKey(Subjects, on_delete = models.CASCADE)

    parent_id_field = 'subject_id'

    def __str__(self):
        return f"{self.user} -> {self.subject}"

    def setParentID(self, parentID):
        self.__dict__.update({ "subject_id": parentID })

    def commentSVG(self):
        return

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
    
    # Object Factory for abstract

    def objectFactory():
        return Comments()


class Ratings(AbstractCRUD):
    value       = models.IntegerField()
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)
    comment     = models.ForeignKey(Comments, on_delete = models.CASCADE)

    parent_id_field = 'comment_id'

    def __str__(self):
        return f"{self.user}, value: {self.value} -> comment in: {self.comment.subject}"

    def setParentID(self, parentID):
        self.__dict__.update({ "comment_id": parentID })

    def toDict(self):
        return {"id": self.id,
                "value": self.value,
                "user_id": self.user.id,
                "author": self.user.login,
                "author_avatar": self.user.avatar,
                "comment_id": self.comment.id,
                "subject": self.comment.subject.name}

    # Create Ratings (validate)

    @classmethod
    def __validateUnique(model, parentID, objectDict):
        objectsAll = model.__allObjectsDict(model)
        for x in objectsAll:
            if model == Ratings:
                if int(x['user_id']) == int(objectDict['user_id']) and int(x['comment_id']) == parentID:
                    return False
        return True


class Transactions(AbstractCRUD):
    price               = models.FloatField(default=255)
    price_forecast      = models.FloatField(default=255)
    currency            = models.CharField(max_length=255)
    date_of_transaction = models.DateTimeField('date of transaction')
    course_on_payment   = models.FloatField(default=255)
    user                = models.ForeignKey(Users, on_delete = models.CASCADE)

    parent_id_field = 'user_id'

    def __str__(self):
        return f"{self.user.login}, cash: {self.price}, prognosis: {self.price_forecast}"

    def setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    def toDict(self):
        return {"id": self.id,
                "price": self.price,
                "currency": self.currency,
                "date_of_transaction": self.date_of_transaction,
                "course_on_payment": self.course_on_payment,
                "user_id": self.user.id,
                "author": self.user.login,
                "exchange_id": self.exchange.id}


class Triggers(AbstractCRUD):
    course_values_for_trigger   = models.FloatField(default=255)
    date_of_trigger             = models.CharField(max_length=255)
    status                      = models.IntegerField(default=1)
    user                        = models.ForeignKey(Users, on_delete = models.CASCADE)

    parent_id_field = 'user_id'

    def __str__(self):
        return f"{self.user.login}, trigger value: {self.course_values_for_trigger}, date: {self.date_of_trigger}"

    def setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    def toDict(self):
        return {"id": self.id,
                "course_values_for_trigger": self.course_values_for_trigger,
                "date_of_trigger": self.date_of_trigger,
                "status": self.status,
                "user_id": self.user.id,
                "author": self.user.login,}

    def _setActualTimeTrigger(self)
        self.date_of_trigger = str(datetime.now().strftime("%Y-%d-%m %H:%M"))


class Notifications(ObjectAbstract):
    message     = models.CharField(max_length=255)
    user        = models.ForeignKey(Users, on_delete = models.CASCADE)

    parent_id_field = 'user_id'

    def __str__(self):
        return f"Message: {self.message}, for User: {self.user.login}"

    def _setParentID(self, parentID):
        self.__dict__.update({ "user_id": parentID })

    def toDict(self):
        return {"id": self.id,
                "message": self.message,
                "user_id": self.user.id}
