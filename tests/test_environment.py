from unittest.mock import MagicMock
from src.environment import Environment
from src.grid import Grid
from src.entity import Entity
from src.location import Location

NORMAL_SIZE=10
LARGE_SIZE=100

# test initializing environment
def test_initialization():
    environment = Environment("test", NORMAL_SIZE)
    assert environment.id != None
    assert environment.name == "test"
    assert environment.grid != None
    assert environment.creationDate != None

def test_initializing_large_environment():
    environment = Environment("large test", LARGE_SIZE)
    assert environment.id != None
    assert environment.name == "large test"
    assert environment.grid != None
    assert environment.creationDate != None

# test getters
def test_getters():
    environment = Environment("test", NORMAL_SIZE)
    assert environment.getID() != None
    assert environment.getName() == "test"
    assert environment.getGrid() != None
    assert environment.getCreationDate() != None

# test setters
def test_setters():
    environment = Environment("test", NORMAL_SIZE)
    environment.setID(1)
    assert environment.getID() == 1
    environment.setName("test2")
    assert environment.getName() == "test2"
    environment.setGrid(Grid(NORMAL_SIZE, NORMAL_SIZE))
    assert environment.getGrid() != None

def test_getting_entity_by_id():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    environment.addEntity(entity)
    assert environment.getEntity(entity.getID()) == entity

def test_getting_entity_by_id_not_present():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    assert environment.getEntity(entity.getID()) == None
