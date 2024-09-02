from unittest.mock import MagicMock
from src.grid import Grid
from src.location import Location
from src.entity import Entity

# test initializing grid
def test_initialization():    
    grid = Grid(10, 10)
    assert grid.id != None
    assert grid.columns == 10
    assert grid.rows == 10
    assert grid.locations != None
    assert grid.getSize() == 100

def test_initialization_large():
    grid = Grid(100, 100)
    assert grid.id != None
    assert grid.columns == 100
    assert grid.rows == 100
    assert grid.locations != None
    assert grid.getSize() == 10000

# test getters
def test_getters():    
    grid = Grid(10, 10)
    assert grid.getID() != None
    assert grid.getColumns() == 10
    assert grid.getRows() == 10
    assert grid.getLocations() != None
    assert grid.getSize() == 100

# test setters
def test_setters():
    grid = Grid(10, 10)
    grid.setID(1)
    assert grid.getID() == 1
    grid.setColumns(5)
    assert grid.getColumns() == 5
    grid.setRows(5)
    assert grid.getRows() == 5
    grid.setLocations([])
    assert grid.getLocations() == []

# def adding an entity to a specific location
def test_adding_an_entity_to_a_specific_location():
    grid = Grid(10, 10)
    entity = Entity("test")
    location = Location(1, 1)
    grid.addLocation(location)
    grid.addEntityToLocation(entity, location)
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1

def test_retrieving_random_location():
    grid = Grid(10, 10)
    location = grid.getRandomLocation()
    assert location != None

def test_retrieving_entity_by_id():
    grid = Grid(10, 10)
    entity = Entity("test")
    grid.addEntity(entity)
    assert grid.getEntity(entity.getID()) == entity

def test_retrieving_entity_by_id_not_present():
    grid = Grid(10, 10)
    entity = Entity("test")
    assert grid.getEntity(entity.getID()) == None

def test_adding_an_entity_to_random_location_in_large_grid():
    # prepare
    grid = Grid(100, 100)
    entity = Entity("test")
    location = grid.getRandomLocation()

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1

def test_retrieving_entity_by_id_in_large_grid():
    # prepare
    grid = Grid(100, 100)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    retrievedEntity = grid.getEntity(entity.getID())

    # verify
    assert entity == retrievedEntity
