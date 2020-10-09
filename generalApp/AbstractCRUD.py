from django.db import models
from django.http import HttpResponse
from datetime import datetime
from .utilities import *


class ValidationUtils():

    @classmethod
    def fromDict(self, dict):
        self.__dict__.update(dict)

    class Meta:
        abstract = True


class AbstractUtilsCRUD():
    """
    This class have a primary utilities for CRUD functionality
    """
    
    @classmethod
    def _objectFactory(self):
        """
        return a new specific object
        """
        pass

    @classmethod
    def _setParentID(self, parentID):
        """
        set object parent id
        """
        pass

    @classmethod
    def _allObjectsDict(self):
        """
        map all class objects to dict
        """
        objectAll = self._objectFactory().objects.all()
        list = []
        for x in objectAll:
            list.append(x.toDict())
        return list
    
    class Meta:
        abstract = True


class AbstractGet(AbstractUtilsCRUD):
    """
    This class have a abstract `getOne` / `getAll` / `getByParent`
    """

    parent_id_field = ''
    
    @classmethod
    def getObject(self, objectID):
        """
        get one object
        """
        return self.__getObjectNormal(self, objectID)

    def __getObjectNormal(self, objectID):
        object = self._objectFactory().objects.get(pk = objectID).toDict()
        return HttpResponse(json.dumps(object))

    @classmethod
    def getAllObjects(self):
        """
        get all objects
        """
        objectsAll = self._allObjectsDict()
        return HttpResponse(json.dumps(objectsAll))

    @classmethod
    def getObjectsByParentID(self, parentID):
        """
        get objects by parent id
        """
        return HttpResponse(self.__getAllByParentID(parentID))
    
    @classmethod
    def __getAllByParentID(self, parentID):
        list = [ 
            x.toDict() 
            for x in self._objectFactory()
            .objects.filter(**{ self._objectFactory().parent_id_field: parentID })
        ]
        return json.dumps(list)

    class Meta:
        abstract = True


class AbstractCreate(AbstractUtilsCRUD):
    """
    This class have a abstract `create`
    """

    @classmethod
    def addObject(self, request, privilige):
        """
        create object without parent
        """
        object = jsonLoad(request)
        if checkSession(request, privilige):
            if self._validateUnique(object):
                 return self._saveObject(object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")

    @classmethod
    def _validateUnique(self, userDict):
        """
        use validate in override this method
        """
        return True
    
    @classmethod
    def _saveObject(self, objectDict):
        """
        save object without parent
        """
        del objectDict['token']
        newObject = self._objectFactory().objects.create(**objectDict)
        self._setActualTimeTrigger(newObject)
        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

    @classmethod
    def _setActualTimeTrigger(self, trigger):
        pass

    @classmethod
    def addObjectWithParent(self, request, parentID, privilige):
        """
        create object with parent
        """
        object = jsonLoad(request)
        if checkSession(request, privilige):
            if self._validateUnique(object):
                 return self._saveObjectWithParent(parentID, object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")
    
    @classmethod
    def _saveObjectWithParent(self, parentID, objectDict):
        """
        save object with parent & subject + comment & set trigger time
        """
        del objectDict['token']
        newObject = self._objectFactory().objects.create(**objectDict)

        self._setParentID(parentID)
        self._createFirstComment(newObject, objectDict)

        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

    @classmethod
    def _createFirstComment(self, newSubject, objectDict):
        pass
    
    class Meta:
        abstract = True


class AbstractUpdate(AbstractUtilsCRUD):
    """
    This class have a abstract `update`
    """

    @classmethod
    def putObject(self, request, objectID, privilige):
        object = jsonLoad(request) 
        if checkSession(request, privilige) or checkUserPermission(object, request):
            return self._updateObject(object, objectID)
        else:
            return HttpResponse("No Permission")
    
    @classmethod
    def _updateObject(self, objectDict, objectID):
        objectOld = self._objectFactory().objects.get(pk = objectID)
        objectOld.fromDict(objectDict)
        objectOld.save()
        return HttpResponse(f"Update Object: {objectOld.toDict()}")

    class Meta:
        abstract = True


class AbstractDelete(AbstractUtilsCRUD):
    """
    This class have a abstract `delete`
    """

    @classmethod
    def deleteObject(self, request, objectID, privilige):
        objectDel = self._objectFactory().objects.get(pk = objectID)
        if checkSession(request, privilige) or checkUserPermission(objectDel.toDict(), request):
            objectDel.delete()
            return HttpResponse(f"Delete Object: {objectDel}")
        else:
            return HttpResponse("No Permission")

    class Meta:
        abstract = True


class AbstractCRUD(
    models.Model,
    AbstractGet,
    AbstractCreate,
    AbstractUpdate,
    AbstractDelete,
):

    @classmethod
    def fromDict(self, dict):
        self.__dict__.update(dict)

    class Meta:
        abstract = True