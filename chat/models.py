from django.db import models
from django.http import HttpResponse
import json

class Lobby(models.Model):
    name        = models.CharField(max_length=30)
    userCount   = models.IntegerField()

    def __str__(self):
        return f"{self.id} {self.name} {self.userCount}"

    def fromDict(self, dict):
        self.__dict__.update(dict)

    def toDict(self):
        return {"id": self.id,
                "name": self.name,
                "userCount": self.userCount}
    
    def allObjectsDict(self):
        objectAll = self.objects.all()
        list = []
        for x in objectAll:
            list.append(x.toDict())
        return json.dumps(list)