from objects.entity import Entity
from objects.environment import Environment

entity = Entity("Gerald")
entity.printInfo()

environment = Environment("test")
environment.addEntity(entity)
environment.printInfo()