from unittest.mock import MagicMock
from src.grid import Grid
from src.location import Location
from src.entity import Entity

NORMAL_SIZE=10
LARGE_SIZE=100

# test initializing grid
def test_initialization():    
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    assert grid.id != None
    assert grid.columns == NORMAL_SIZE
    assert grid.rows == NORMAL_SIZE
    assert grid.locations != None
    assert grid.getSize() == NORMAL_SIZE * NORMAL_SIZE

def test_initialization_large():
    grid = Grid(LARGE_SIZE, LARGE_SIZE)
    assert grid.id != None
    assert grid.columns == LARGE_SIZE
    assert grid.rows == LARGE_SIZE
    assert grid.locations != None
    assert grid.getSize() == LARGE_SIZE * LARGE_SIZE

# test getters
def test_getters():    
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    assert grid.getID() != None
    assert grid.getColumns() == NORMAL_SIZE
    assert grid.getRows() == NORMAL_SIZE
    assert grid.getLocations() != None
    assert grid.getSize() == NORMAL_SIZE * NORMAL_SIZE

# test setters
def test_setters():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
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
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = Location(1, 1)
    grid.addLocation(location)
    grid.addEntityToLocation(entity, location)
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1

def test_retrieving_random_location():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    assert location != None

def test_retrieving_entity_by_id():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    assert grid.getEntity(entity.getID()) == entity

def test_retrieving_entity_by_id_not_present():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    assert grid.getEntity(entity.getID()) == None

def test_adding_an_entity_to_random_location_in_large_grid():
    # prepare
    grid = Grid(LARGE_SIZE, LARGE_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1

def test_retrieving_entity_by_id_in_large_grid():
    # prepare
    grid = Grid(LARGE_SIZE, LARGE_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    retrievedEntity = grid.getEntity(entity.getID())

    # verify
    assert entity == retrievedEntity

def test_getLocationByCoordinates():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    targetX = NORMAL_SIZE / 2
    targetY = NORMAL_SIZE / 2

    # execute
    retrievedLocation = grid.getLocationByCoordinates(targetX, targetY)

    # verify
    assert retrievedLocation != None
    assert retrievedLocation.getX() == targetX
    assert retrievedLocation.getY() == targetY

def test_getLocationByCoordinates_LargeGrid():
    # prepare
    grid = Grid(LARGE_SIZE, LARGE_SIZE)
    targetX = NORMAL_SIZE / 2
    targetY = NORMAL_SIZE / 2

    # execute
    retrievedLocation = grid.getLocationByCoordinates(targetX, targetY)

    # verify
    assert retrievedLocation != None
    assert retrievedLocation.getX() == targetX
    assert retrievedLocation.getY() == targetY

def test_isEntityPresent():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    isPresent = grid.isEntityPresent(entity)

    # verify
    assert isPresent == True