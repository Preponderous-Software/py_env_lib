# Copyright (c) 2022 Preponderous Software
# MIT License
from entity import Entity
from environment import Environment


# create environment
environment = Environment("My World")
print("Created environment.")

# create entity
entity = Entity("Gerald")
print("Created entity.")

# place entity
environment.addEntity(entity)
print("Placed entity into environment.")

# check for expected behavior
assert(environment.getNumEntities() == 1)
assert(entity.getEnvironmentID() == environment.getID())
assert(entity.getGridID() == environment.getGrid().getID())
assert(entity.getLocationID() == environment.getGrid().getFirstLocation().getID())
print("Assertions passed.")