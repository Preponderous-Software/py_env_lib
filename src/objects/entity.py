# Copyright (c) 2022 Preponderous Software
# MIT License

# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import datetime
import random


class Entity(object):

    def __init__(self, name):
        self.id = random.randint(0, 999)
        self.name = name
        self.creationDate = datetime.datetime.now()
        self.environmentID = random.randint(0, 999)
        self.locationID = random.randint(0, 999)
    
    def getID(self):
        return self.id
    
    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def getCreationDate(self):
        return self.creationDate

    def getEnvironmentID(self):
        return self.environmentID

    def setEnvironmentID(self, environmentID):
        self.environmentID = environmentID

    def getLocationID(self):
        return self.locationID

    def setLocationID(self, locationID):
        self.locationID = locationID
    
    def printInfo(self):
        print("--------------")
        print(self.name)
        print("--------------")
        print("ID: ", self.getID())
        print("Creation Date: ", self.getCreationDate())
        print("Environment ID: ", self.getEnvironmentID())
        print("Location ID: ", self.getLocationID())
        print("\n")