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

def test_isEntityPresent_not_present():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")

    # execute
    isPresent = grid.isEntityPresent(entity)

    # verify
    assert isPresent == False

def test_getFirstLocation():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location != None
    assert location.getID() in grid.getLocations()

def test_removeLocation():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    sizeBefore = grid.getSize()

    # execute
    grid.removeLocation(location)

    # verify
    assert grid.getSize() == sizeBefore - 1
    assert location.getID() not in grid.getLocations()

def test_addLocation():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    sizeBefore = grid.getSize()

    # execute
    grid.addLocation(location)

    # verify
    assert grid.getSize() == sizeBefore + 1
    assert location.getID() in grid.getLocations()

def test_getLocation():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()

    # execute
    retrievedLocation = grid.getLocation(location.getID())

    # verify
    assert retrievedLocation == location

def test_grid_removeEntity():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == False
    assert location.getNumEntities() == 0

def test_grid_removeEntity_not_present():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == False

# test navigating the grid
def test_getUp():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    up = grid.getUp(location)

    # verify
    assert up.getX() == 1
    assert up.getY() == 0

def test_getUp_at_top_edge():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(0, 0)

    # execute
    up = grid.getUp(location)

    # verify
    assert up == -1

def test_getUp_invalid_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    up = grid.getUp(-1)

    # verify
    assert up == -1

def test_getDown():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    down = grid.getDown(location)

    # verify
    assert down.getX() == 1
    assert down.getY() == 2

def test_getDown_at_bottom_edge():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(0, NORMAL_SIZE - 1)

    # execute
    down = grid.getDown(location)

    # verify
    assert down == -1

def test_getDown_invalid_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    down = grid.getDown(-1)

    # verify
    assert down == -1

def test_getLeft():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    left = grid.getLeft(location)

    # verify
    assert left.getX() == 0
    assert left.getY() == 1

def test_getLeft_at_left_edge():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(0, 0)

    # execute
    left = grid.getLeft(location)

    # verify
    assert left == -1

def test_getLeft_invalid_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    left = grid.getLeft(-1)

    # verify
    assert left == -1

def test_getRight():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    right = grid.getRight(location)

    # verify
    assert right.getX() == 2
    assert right.getY() == 1

def test_getRight_at_right_edge():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(NORMAL_SIZE - 1, 0)

    # execute
    right = grid.getRight(location)

    # verify
    assert right == -1

def test_getRight_invalid_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    right = grid.getRight(-1)

    # verify
    assert right == -1