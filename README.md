# Trade App
Python / Django / Websocket / Docker / Own REST / Own App Security

## Basic Information

Application for analyze a BTC stock exchange & community. Thanks this app you can subscribe BTC exchange and you can contact quickly with other app users (websocket chat & rest forum). Functionality has:
- chart (candles)
- triggers (it's create a notification when stock exchange get a your value)
- basic prognosis
- notifications

Trade App has also security func (like create/verify tokens (hashed information about user and session))

### Project Structure

```bash
.
├── chat
│   ├── admin.py
│   ├── consumers.py
│   ├── models.py
│   ├── routing.py
│   ├── urls.py
│   └── views.py
├── generalApp
│   ├── AbstractCRUD.py
│   ├── admin.py
│   ├── apps.py
│   ├── exchangeVO.py
│   ├── methods.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── utilities.py
│   └── views.py
├── manage.py
├── migrate.sh
├── packages.sh
├── run.sh
└── TradeApp
    ├── routing.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

### UML

![uml_by_apps](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/12abb353-ab91-4433-96d3-b5d9c5847254/de56rda-8c6c1a01-e952-4957-9890-c19519eeeae5.png/v1/fill/w_1280,h_864,strp/class_diagram_by_apps_by_00x097_de56rda-fullview.png?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1cm46YXBwOiIsImlzcyI6InVybjphcHA6Iiwib2JqIjpbW3siaGVpZ2h0IjoiPD04NjQiLCJwYXRoIjoiXC9mXC8xMmFiYjM1My1hYjkxLTQ0MzMtOTZkMy1iNWQ5YzU4NDcyNTRcL2RlNTZyZGEtOGM2YzFhMDEtZTk1Mi00OTU3LTk4OTAtYzE5NTE5ZWVlYWU1LnBuZyIsIndpZHRoIjoiPD0xMjgwIn1dXSwiYXVkIjpbInVybjpzZXJ2aWNlOmltYWdlLm9wZXJhdGlvbnMiXX0.2Jm_XxFhksN8mAtdUS9n_F0shiK8VttfN21rhm1-tbk)

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

It're a utils for CRUD classes using global like this:

```python

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
        
```

```python

class AbstractCreate(AbstractUtilsCRUD):
    """
    This class have a abstract `create`
    """

    [...]
    
    @classmethod
    def _saveObject(self, objectDict):
        """
        save object without parent
        """
        del objectDict['token']
        newObject = self._objectFactory().objects.create(**objectDict)
        
        [...]
        
        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

```
Other classes looks similar to AbstractCreate / AbstractGet (let's see AbstractCRUD for more details).

Generaly - I'm gonna refactor this app with design patterns like:
- chain of responsibility (thanks tree structure classes, possible go this way: endpoint request -> verify user (security functionality) -> app functionality)
- wrapper (this pattern will be helpfull in the future when I will expanded app for more stock exchanges)
- strategy (for swapping functionality in functionality classes with many `if` statements)
