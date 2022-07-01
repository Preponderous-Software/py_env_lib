# Copyright (c) 2022 Preponderous Software
# MIT License
import datetime
import random
from objects.entity import Entity
from objects.grid import Grid


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
class Environment(object):

    def __init__(self, name):
        self.id = random.randint(0, 100)
        self.name = name
        self.grid = Grid(self, 2, 2)
        self.creationDate = datetime.datetime.now()
        self.entities = []
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def getCreationDate(self):
        return self.creationDate

    def getGrid(self):
        return self.grid

    def setID(self, id):
        self.id = id

    def setName(self, name):
        self.name = name

    def setGrid(self, grid):
        self.grid = grid

    def addEntity(self, entity: Entity):
        self.entities.append(entity)
    
    def removeEntity(self, entity: Entity):
        self.entities.remove(entity)
    
    def isEntityPresent(self, entity: Entity):
        return entity.getID() in self.entities

    def getNumEntities(self):
        return len(self.entities)

    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Grid ID: ", self.getGrid().getID())
        print("Num entities: ", self.getNumEntities())
        print("\n")