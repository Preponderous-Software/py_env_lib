# Copyright (c) 2022 Preponderous Software
# MIT License


# @author Daniel McCoy Stephenson
# @since July 1st, 2022
import random


class Grid(object):

    def __init__(self, columns, rows, parentEnvironment):
        self.id = random.randint(0, 100)
        self.columns = columns
        self.rows = rows
        self.parentEnvironment = parentEnvironment
        self.locationIDs = []

    def getID(self):
        return self.id

    def getColumns(self):
        return self.columns

    def getRows(self):
        return self.rows
    
    def getParentEnvironment(self):
        return self.parentEnvironment

    def getLocationIDs(self):
        return self.locationIDs

    def getFirstLocationID(self):
        return self.locationIDs.pop()
    
    def setID(self, id):
        self.id = id
    
    def setColumns(self, columns):
        self.columns = columns;
    
    def setRows(self, rows):
        self.rows = rows;
    
    def setParentEnvironment(self, parentEnvironment):
        self.parentEnvironment = parentEnvironment
    
    def setLocationIDs(self, locationIDs):
        self.locationIDs = locationIDs
    
    def addLocationID(self, locationID):
        self.locationsIDs.append(locationID)
    
    def removeLocationID(self, locationID):
        self.locationIDs.remove(locationID)

    def toString(self):
        pass # TODO: implement