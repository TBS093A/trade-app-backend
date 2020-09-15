# Trade App
Python / Django / Websocket / Docker / Own REST / Own App Security

## Basic Information

Application for analyze a BTC stock exchange & community. Thanks this app you can subscribe BTC exchange and you can contact quickly with other app users (websocket chat & rest forum). Functionality has:
- chart (candles)
- triggers (it's create a notification when stock exchange get a your value)
- basic prognosis
- notifications

### Project Structure

### UML

## Comments

Application need a refactor endpoints, general functionality and security. General structure -> "generalApp" will be smashed a smaller apps/directores. Now, CRUD has been refactorized full, you can see:

```python

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
```

It's a utils for CRUD classes using global like this:

```python
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
```
Other classes looks similar to AbstractCreate (let's see AbstractCRUD for more details).

Generaly - I'm gonna refactor this app with design patterns like:
- chain of responsibility (thanks tree structure classes, possible go this way: endpoint request -> verify user (security functionality) -> app functionality)
- wrapper (this pattern will be helpfull in the future when I will expanded app for more stock exchanges)
- strategy (for swapping functionality in functionality classes with many `if` statements)
