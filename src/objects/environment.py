# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import random
from objects.entity import Entity

# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class Environment(object):

    def __init__(self, name):
        self.id = random.randint(0, 100)
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.gridID = random.randint(0, 100)
        self.entityIDs = []
    
    def getID(self):
        return self.id

    def setID(self, id):
        self.id = id
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getCreationDate(self):
        return self.creationDate

    def getGridID(self):
        return self.gridID

    def setGridID(self, locationID):
        self.locationID = locationID

    def addEntity(self, entity: Entity):
        self.entityIDs.append(entity.getID())
    
    def removeEntity(self, entity: Entity):
        self.entityIDs.remove(entity.getID())
    
    def isEntityPresent(self, entity: Entity):
        return entity.getID() in self.entityUUIDs

    def getNumEntities(self):
        return len(self.entityIDs)

    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Grid ID: ", self.getGridID())
        print("Num entities: ", self.getNumEntities())
        print("\n")