from unittest.mock import MagicMock
from src.grid import Grid
from src.location import Location
from src.entity import Entity

NORMAL_SIZE=10
LARGE_SIZE=100
RECT_COLUMNS=3
RECT_ROWS=5

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

def test_initialization_rectangular():
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    assert grid.getColumns() == RECT_COLUMNS
    assert grid.getRows() == RECT_ROWS
    assert grid.getSize() == RECT_COLUMNS * RECT_ROWS

def test_generateLocations_rectangular_coordinates():
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    coordinates = set()
    for location in grid.getLocations().values():
        coordinates.add((location.getX(), location.getY()))
    expected = set()
    for x in range(RECT_COLUMNS):
        for y in range(RECT_ROWS):
            expected.add((x, y))
    assert coordinates == expected

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

def test_setLocations_replaces_the_locations_used_by_lookups():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    oldLocation = grid.getLocationByCoordinates(0, 0)
    newLocation = Location(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    grid.setLocations({newLocation.getID(): newLocation})

    # verify
    assert grid.getSize() == 1
    assert grid.getFirstLocation() == newLocation
    assert grid.getLocation(newLocation.getID()) == newLocation
    assert grid.getLocationByCoordinates(NORMAL_SIZE, NORMAL_SIZE) == newLocation
    assert grid.getLocationByCoordinates(0, 0) == -1
    assert oldLocation.getID() not in grid.getLocations()

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

def test_adding_an_entity_to_the_same_location_twice_is_not_duplicated():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    grid.addEntityToLocation(entity, location)

    # verify
    assert grid.getNumEntities() == 1
    assert location.getNumEntities() == 1

def test_adding_an_entity_to_a_location_uses_the_grids_stored_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    storedLocation = grid.getRandomLocation()
    lookalikeLocation = Location(storedLocation.getX(), storedLocation.getY())
    lookalikeLocation.id = storedLocation.getID()

    # execute
    grid.addEntityToLocation(entity, lookalikeLocation)

    # verify
    assert storedLocation.isEntityPresent(entity)
    assert lookalikeLocation.getNumEntities() == 0
    assert entity.getLocationID() == storedLocation.getID()

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

def test_adding_an_entity_to_a_random_location_sets_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")

    # execute
    grid.addEntity(entity)

    # verify
    assert entity.getGridID() == grid.getID()
    location = grid.getLocation(entity.getLocationID())
    assert location != None
    assert location.isEntityPresent(entity)
    assert grid.isEntityPresent(entity)

def test_retrieving_random_location():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    assert location != None

def test_retrieving_random_location_returns_a_location_in_the_grid():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    location = grid.getRandomLocation()

    # verify
    assert grid.getLocations()[location.getID()] is location

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

def test_retrieving_entity_by_id_from_a_grid_with_no_locations():
    # prepare
    grid = Grid(0, 0)
    entity = Entity("test")

    # execute
    retrievedEntity = grid.getEntity(entity.getID())

    # verify
    assert retrievedEntity == None

def test_retrieving_entity_by_id_after_removal():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)

    # execute
    grid.removeEntity(entity)

    # verify
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

def test_getLocationByCoordinates_out_of_bounds():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)

    # execute and verify
    assert grid.getLocationByCoordinates(RECT_COLUMNS, 0) == -1
    assert grid.getLocationByCoordinates(0, RECT_ROWS) == -1
    assert grid.getLocationByCoordinates(-1, 0) == -1
    assert grid.getLocationByCoordinates(0, -1) == -1

def test_getLocationByCoordinates_out_of_bounds_is_silent(capsys):
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    capsys.readouterr()

    # execute
    retrievedLocation = grid.getLocationByCoordinates(RECT_COLUMNS, RECT_ROWS)

    # verify
    assert retrievedLocation == -1
    assert capsys.readouterr().out == ""

def test_getLocationByCoordinates_rectangular_corner():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)

    # execute
    retrievedLocation = grid.getLocationByCoordinates(RECT_COLUMNS - 1, RECT_ROWS - 1)

    # verify
    assert retrievedLocation.getX() == RECT_COLUMNS - 1
    assert retrievedLocation.getY() == RECT_ROWS - 1

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

def test_isEntityPresent_after_removal():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntityToLocation(entity, grid.getRandomLocation())
    grid.removeEntity(entity)

    # execute
    isPresent = grid.isEntityPresent(entity)

    # verify
    assert isPresent == False

def test_isEntityPresent_after_removing_its_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)
    grid.removeLocation(location)

    # execute
    isPresent = grid.isEntityPresent(entity)

    # verify
    assert isPresent == False
    assert location.isEntityPresent(entity) == True

def test_getFirstLocation():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location != None
    assert location.getID() in grid.getLocations()

def test_getFirstLocation_from_a_grid_with_no_locations():
    # prepare
    grid = Grid(0, 0)

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location == None

def test_getFirstLocation_from_a_grid_with_no_locations_warns(capsys):
    # prepare
    grid = Grid(0, 0)
    capsys.readouterr()

    # execute
    grid.getFirstLocation()

    # verify
    assert capsys.readouterr().out == "Warning: A grid had no locations when attempting to retrieve the first location from it.\n"

def test_getFirstLocation_from_a_grid_whose_locations_were_all_removed():
    # prepare
    grid = Grid(1, 1)
    grid.removeLocation(grid.getFirstLocation())

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location == None

def test_getFirstLocation_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    capsys.readouterr()

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location != None
    assert capsys.readouterr().out == ""

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

def test_addLocation_already_present_is_not_duplicated():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getRandomLocation()
    sizeBefore = grid.getSize()

    # execute
    grid.addLocation(location)

    # verify
    assert grid.getSize() == sizeBefore
    assert grid.getLocation(location.getID()) == location

def test_addLocation_is_reachable_by_coordinates_and_navigation():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    location = Location(RECT_COLUMNS, 0)
    edgeLocation = grid.getLocationByCoordinates(RECT_COLUMNS - 1, 0)

    # execute
    grid.addLocation(location)

    # verify
    assert grid.getLocationByCoordinates(RECT_COLUMNS, 0) == location
    assert grid.getRight(edgeLocation) == location
    assert grid.getLeft(location) == edgeLocation

def test_getLocationByCoordinates_after_removing_that_location():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    grid.removeLocation(location)

    # verify
    assert grid.getLocationByCoordinates(1, 1) == -1

def test_getNumEntities_after_removing_a_location_with_an_entity():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    locations = list(grid.getLocations().values())
    grid.addEntityToLocation(Entity("first"), locations[0])
    grid.addEntityToLocation(Entity("second"), locations[1])

    # execute
    grid.removeLocation(locations[0])

    # verify
    assert grid.getNumEntities() == 1

def test_retrieving_entity_by_id_after_removing_its_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    grid.removeLocation(location)

    # verify
    assert grid.getEntity(entity.getID()) == None

def test_removeLocation_with_an_entity_preserves_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = grid.getRandomLocation()
    grid.addEntityToLocation(entity, location)

    # execute
    grid.removeLocation(location)

    # verify
    assert entity.getGridID() == grid.getID()
    assert entity.getLocationID() == location.getID()

def test_getNumEntities_of_a_new_grid():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    numEntities = grid.getNumEntities()

    # verify
    assert numEntities == 0

def test_getNumEntities_after_removing_an_entity():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    locations = list(grid.getLocations().values())
    entity = Entity("first")
    grid.addEntityToLocation(entity, locations[0])
    grid.addEntityToLocation(Entity("second"), locations[1])

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.getNumEntities() == 1

def test_getNumEntities_counts_entities_across_locations():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    locations = list(grid.getLocations().values())
    grid.addEntityToLocation(Entity("first"), locations[0])
    grid.addEntityToLocation(Entity("second"), locations[0])
    grid.addEntityToLocation(Entity("third"), locations[1])

    # execute
    numEntities = grid.getNumEntities()

    # verify
    assert numEntities == 3

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

def test_grid_removeEntity_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntityToLocation(entity, grid.getRandomLocation())
    capsys.readouterr()

    # execute
    grid.removeEntity(entity)

    # verify
    assert capsys.readouterr().out == ""

def test_grid_removeEntity_not_present_is_silent(capsys):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    capsys.readouterr()

    # execute
    grid.removeEntity(entity)

    # verify
    assert capsys.readouterr().out == ""

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

def test_getRight_at_right_edge_of_rectangular_grid():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    location = grid.getLocationByCoordinates(RECT_COLUMNS - 1, 0)

    # execute
    right = grid.getRight(location)

    # verify
    assert right == -1

def test_getDown_at_bottom_edge_of_rectangular_grid():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    location = grid.getLocationByCoordinates(0, RECT_ROWS - 1)

    # execute
    down = grid.getDown(location)

    # verify
    assert down == -1

def test_navigating_there_and_back_returns_the_same_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)

    # execute
    upAndBack = grid.getDown(grid.getUp(location))
    rightAndBack = grid.getLeft(grid.getRight(location))

    # verify
    assert upAndBack is location
    assert rightAndBack is location

def test_navigating_from_a_location_not_in_the_grid_uses_its_coordinates():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    foreignLocation = Location(1, 1)

    # execute
    right = grid.getRight(foreignLocation)

    # verify
    assert right is grid.getLocationByCoordinates(2, 1)
    assert right.getID() in grid.getLocations()

def test_navigating_into_a_removed_location():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(1, 1)
    grid.removeLocation(grid.getLocationByCoordinates(1, 0))

    # execute
    up = grid.getUp(location)

    # verify
    assert up == -1