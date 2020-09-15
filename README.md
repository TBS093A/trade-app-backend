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
        self._setActualTimeTrigger(newObject)
        newObject.save()
        return HttpResponse(f"Add new Object: {newObject.toDict()}")

```
Other classes looks similar to AbstractCreate (let's see AbstractCRUD for more details).

Generaly - I'm gonna refactor this app with design patterns like:
- chain of responsibility (thanks tree structure classes, possible go this way: endpoint request -> verify user (security functionality) -> app functionality)
- wrapper (this pattern will be helpfull in the future when I will expanded app for more stock exchanges)
- strategy (for swapping functionality in functionality classes with many `if` statements)
