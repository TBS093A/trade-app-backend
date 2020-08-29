from django.db import models

class AbstractUtilsCRUD():
    """
    This class have a primary utilities for CRUD functionality
    """
    
    @classmethod
    def objectFactory(self):
        """
        return a new specific object
        """
        pass

    @classmethod
    def setParentID(self, parentID):
        """
        set object parent id
        """
        pass

    @classmethod
    def allObjectsDict(self):
        """
        map all class objects to dict
        """
        objectAll = self.objectFactory().objects.all()
        list = []
        for x in objectAll:
            list.append(x.toDict())
        return list


class AbstractGet(AbstractUtilsCRUD):
    """
    This class have a abstract getOne / getAll / getByParent
    """

    parent_id_field = ''
    
    @classmethod
    def getObject(self, objectID):
        """
        get one object
        """
        return self.__getObjectNormal(self, objectID)

    def __getObjectNormal(self, objectID):
        object = self.objectFactory().objects.get(pk = objectID).toDict()
        return HttpResponse(json.dumps(object))

    @classmethod
    def getAllObjects(self):
        """
        get all objects
        """
        objectsAll = self.allObjectsDict()
        return HttpResponse(json.dumps(objectsAll))

    @classmethod
    def getObjectsByParentID(self, parentID):
        """
        get objects by parent id
        """
        return HttpResponse(self.__getAllByParentID(parentID))
    
    def __getAllByParentID(self, parentID):
        list = [ x.toDict() for x in self.objectFactory()
            .__get.objects.filter(**{ parent_id_field: parentID })]
        return json.dumps(list)


class AbstractCreate(AbstractUtilsCRUD):

    @classmethod
    def addObject(request, privilige):
        object = jsonLoad(request)
        if checkSession(request, privilige):
            if self.__validateUnique(object):
                 return self.__saveObject(object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")

    @classmethod
    def __validateUnique(self, userDict):
        return True

    @classmethod
    def __saveObject(self, objectDict):
        newObject = self.__getObject()
        newObject.fromDict(objectDict)
        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

    @classmethod
    def __saveObject(self, parentID, objectDict):
        newObject = self.__getObject()
        newObject.fromDict(objectDict)

        self.__setParentID(parentID)
        self.__createFirstComment(newObject, objectDict)
        self.__setActualTimeTrigger()

        newObject.save()
        return HttpResponse(f"Add new Subject: {newObject.toDict()} -> {newComment.toDict()}")

    @classmethod
    def __createFirstComment(newSubject, objectDict):
        pass

    @classmethod
    def __setActualTimeTrigger():
        pass


class AbstractUpdate(AbstractUtilsCRUD):
    pass


class AbstractDelete(AbstractUtilsCRUD):
    pass


class AbstractCRUD(
    models.Model,
    AbstractGet,
    AbstractCreate,
    AbstractUpdate,
    AbstractDelete,
):
    pass