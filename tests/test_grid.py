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

def test_adding_an_entity_to_a_location_not_in_the_grid():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = Location(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert grid.getNumEntities() == 0
    assert location.getNumEntities() == 0
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_adding_an_entity_to_a_location_not_in_the_grid_warns(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    capsys.readouterr()

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert capsys.readouterr().out == "Warning: A location was not present when attempting to add an entity to it in a grid.\n"

def test_adding_an_entity_to_a_specific_location_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    capsys.readouterr()

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert capsys.readouterr().out == ""
    assert entity.getGridID() == grid.getID()

def test_adding_an_entity_to_a_grid_with_no_locations():
    # prepare
    grid = Grid(0, 0)
    entity = Entity("test")

    # execute
    grid.addEntity(entity)

    # verify
    assert grid.getNumEntities() == 0
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_adding_an_entity_to_a_grid_with_no_locations_warns(capsys):
    # prepare
    grid = Grid(0, 0)
    entity = Entity("test")
    capsys.readouterr()

    # execute
    grid.addEntity(entity)

    # verify
    assert capsys.readouterr().out == "Warning: A grid had no locations when attempting to add an entity to it.\n"

def test_adding_an_entity_to_a_grid_whose_locations_were_all_removed():
    # prepare
    grid = Grid(1, 1)
    entity = Entity("test")
    grid.removeLocation(grid.getFirstLocation())

    # execute
    grid.addEntity(entity)

    # verify
    assert grid.getSize() == 0
    assert grid.getNumEntities() == 0
    assert entity.getGridID() == -1

def test_adding_an_entity_to_a_random_location_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    capsys.readouterr()

    # execute
    grid.addEntity(entity)

    # verify
    assert capsys.readouterr().out == ""
    assert grid.getNumEntities() == 1

def test_retrieving_random_location():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    assert location != None

def test_retrieving_random_location_from_a_grid_with_no_locations():
    # prepare
    grid = Grid(0, 0)

    # execute
    location = grid.getRandomLocation()

    # verify
    assert location == None

def test_retrieving_random_location_from_a_grid_with_no_locations_warns(capsys):
    # prepare
    grid = Grid(0, 0)
    capsys.readouterr()

    # execute
    grid.getRandomLocation()

    # verify
    assert capsys.readouterr().out == "Warning: A grid had no locations when attempting to retrieve a random location from it.\n"

def test_retrieving_random_location_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    capsys.readouterr()

    # execute
    location = grid.getRandomLocation()

    # verify
    assert location != None
    assert capsys.readouterr().out == ""

def test_retrieving_entity_by_id():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    assert grid.getEntity(entity.getID()) == entity

def test_retrieving_entity_by_id_not_present():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    assert grid.getEntity(entity.getID()) == None

def test_retrieving_entity_by_id_not_present_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    capsys.readouterr()

    # execute
    retrievedEntity = grid.getEntity(entity.getID())

    # verify
    assert retrievedEntity == None
    assert capsys.readouterr().out == ""

def test_retrieving_entity_by_id_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    capsys.readouterr()

    # execute
    retrievedEntity = grid.getEntity(entity.getID())

    # verify
    assert retrievedEntity == entity
    assert capsys.readouterr().out == ""

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

def test_removeLocation_not_present():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    sizeBefore = grid.getSize()

    # execute
    grid.removeLocation(location)

    # verify
    assert grid.getSize() == sizeBefore
    assert location.getID() not in grid.getLocations()

def test_removeLocation_not_present_warns(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    capsys.readouterr()

    # execute
    grid.removeLocation(location)

    # verify
    assert capsys.readouterr().out == "Warning: A location was not present when attempting to remove it from a grid.\n"

def test_removeLocation_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    capsys.readouterr()

    # execute
    grid.removeLocation(location)

    # verify
    assert capsys.readouterr().out == ""

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

def test_getLocation_not_present():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    retrievedLocation = grid.getLocation(location.getID())

    # verify
    assert retrievedLocation == None

def test_getLocation_not_present_warns(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    capsys.readouterr()

    # execute
    grid.getLocation(location.getID())

    # verify
    assert capsys.readouterr().out == "Warning: A location was not present when attempting to retrieve it from a grid.\n"

def test_getLocation_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    capsys.readouterr()

    # execute
    retrievedLocation = grid.getLocation(location.getID())

    # verify
    assert retrievedLocation == location
    assert capsys.readouterr().out == ""

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

def test_grid_removeEntity_clears_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)
    assert entity.getGridID() == grid.getID()
    assert entity.getLocationID() == location.getID()

    # execute
    grid.removeEntity(entity)

    # verify
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_grid_removeEntity_removes_every_occurrence():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    locations = list(grid.getLocations().values())
    grid.addEntityToLocation(entity, locations[0])
    grid.addEntityToLocation(entity, locations[1])
    assert grid.getNumEntities() == 2

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == False
    assert grid.getNumEntities() == 0
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_grid_removeEntity_not_present_preserves_containment_ids():
    # prepare
    occupiedGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = occupiedGrid.getRandomLocation()
    occupiedGrid.addEntityToLocation(entity, location)

    # execute
    otherGrid.removeEntity(entity)

    # verify
    assert entity.getGridID() == occupiedGrid.getID()
    assert entity.getLocationID() == location.getID()

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