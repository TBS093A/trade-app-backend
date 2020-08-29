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
        list = [ 
            x.toDict() 
            for x in self.objectFactory()
            .__get.objects.filter(**{ parent_id_field: parentID })
        ]
        return json.dumps(list)


class AbstractCreate(AbstractUtilsCRUD):
    """
    This class have a abstract `create`
    """

    @classmethod
    def addObject(request, privilige):
        """
        create object
        """
        object = jsonLoad(request)
        if checkSession(request, privilige):
            if self.validateUnique(object):
                 return self.saveObject(object)
            else:
                return HttpResponse("Object Is Already Exist")
        else:
            return HttpResponse("No Permission")

    def validateUnique(self, userDict):
        """
        use validate in override this method
        """
        return True

    def saveObject(self, objectDict):
        """
        save object without parent
        """
        newObject = self.objectFactory()
        newObject.fromDict(objectDict)
        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

    def saveObject(self, parentID, objectDict):
        """
        save object with parent & subject + comment & set trigger time
        """
        newObject = self.objectFactory()
        newObject.fromDict(objectDict)

        self.setParentID(parentID)
        self.createFirstComment(newObject, objectDict)
        self.setActualTimeTrigger()

        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

    def createFirstComment(newSubject, objectDict):
        pass

    def setActualTimeTrigger():
        pass


class AbstractUpdate(AbstractUtilsCRUD):
    """
    This class have a abstract `update`
    """

    @classmethod
    def updateObject(self, objectDict, objectID):
        objectOld = self.objectFactory().objects.get(pk = objectID)
        objectOld.fromDict(objectDict)
        if checkSession(request, privilige) and checkUserPermission(objectDel.toDict(), request):
            objectOld.save()
            return HttpResponse(f"Update Object: {objectOld.toDict()}")
        else
            return HttpResponse("No Permission")


class AbstractDelete(AbstractUtilsCRUD):
    """
    This class have a abstract `delete`
    """

    @classmethod
    def deleteObject(self, request, objectID, privilige):
        objectDel = self.objectFactory().objects.get(pk = objectID)
        if checkSession(request, privilige) and checkUserPermission(objectDel.toDict(), request):
            objectDel.delete()
            return HttpResponse(f"Delete Object: {objectDel}")
        else:
            return HttpResponse("No Permission")


class AbstractCRUD(
    models.Model,
    AbstractGet,
    AbstractCreate,
    AbstractUpdate,
    AbstractDelete,
):
    pass