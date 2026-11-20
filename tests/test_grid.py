import uuid
from unittest.mock import MagicMock
import pytest
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

def test_initialization_assigns_a_uuid():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    assert isinstance(grid.getID(), uuid.UUID)

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

def test_generateLocations_orders_locations_by_column_then_row():
    # prepare
    grid = Grid(2, 2)

    # execute
    coordinates = [(location.getX(), location.getY()) for location in grid.getLocations().values()]

    # verify
    assert coordinates == [(0, 0), (0, 1), (1, 0), (1, 1)]

# test grids with an empty or negative dimension
# The constructor does not validate its arguments; a dimension of zero or less yields no locations.
@pytest.mark.parametrize("columns, rows", [(RECT_COLUMNS, 0), (0, RECT_ROWS)])
def test_initialization_with_one_empty_dimension_has_no_locations(columns, rows):
    # execute
    grid = Grid(columns, rows)

    # verify
    assert grid.getSize() == 0
    assert grid.getColumns() == columns
    assert grid.getRows() == rows

@pytest.mark.parametrize("columns, rows", [(-1, RECT_ROWS), (RECT_COLUMNS, -2)])
def test_initialization_with_a_negative_dimension_keeps_it_and_has_no_locations(columns, rows):
    # execute
    grid = Grid(columns, rows)

    # verify
    assert grid.getSize() == 0
    assert grid.getColumns() == columns
    assert grid.getRows() == rows

def test_adding_an_entity_to_a_grid_with_one_empty_dimension_preserves_containment_ids():
    # prepare
    grid = Grid(RECT_COLUMNS, 0)
    entity = Entity("test")

    # execute
    grid.addEntity(entity)

    # verify
    assert grid.getNumEntities() == 0
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

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

def test_setLocations_with_an_entity_preserves_containment_ids():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    locationID = entity.getLocationID()

    grid.setLocations(dict())
    assert grid.isEntityPresent(entity) == False
    assert entity.getGridID() == grid.getID()
    assert entity.getLocationID() == locationID

def test_setLocations_preserves_columns_and_rows():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(0, 0)

    # execute
    grid.setLocations({location.getID(): location})

    # verify
    assert grid.getColumns() == NORMAL_SIZE
    assert grid.getRows() == NORMAL_SIZE
    assert grid.getSize() == 1

def test_setColumns_does_not_regenerate_locations():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    grid.setColumns(RECT_COLUMNS)

    # verify
    assert grid.getColumns() == RECT_COLUMNS
    assert grid.getSize() == NORMAL_SIZE * NORMAL_SIZE
    assert grid.getLocationByCoordinates(NORMAL_SIZE - 1, 0) != -1

def test_setRows_does_not_regenerate_locations():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute
    grid.setRows(RECT_ROWS)

    # verify
    assert grid.getRows() == RECT_ROWS
    assert grid.getSize() == NORMAL_SIZE * NORMAL_SIZE
    assert grid.getLocationByCoordinates(0, NORMAL_SIZE - 1) != -1

def test_setID_applies_only_to_entities_added_afterwards():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    originalID = grid.getID()
    earlier = Entity("earlier")
    later = Entity("later")
    grid.addEntity(earlier)

    # execute
    grid.setID("new-grid-id")
    grid.addEntity(later)

    # verify
    assert earlier.getGridID() == originalID
    assert later.getGridID() == "new-grid-id"
    assert grid.isEntityPresent(earlier)
    assert grid.isEntityPresent(later)

def test_removeEntity_after_setID_clears_grid_id():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    grid.setID("new-grid-id")

    # execute
    grid.removeEntity(entity)

    # verify
    assert entity.getGridID() == -1
    assert not grid.isEntityPresent(entity)

def test_entity_setID_leaves_the_entity_under_its_original_id():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    originalID = entity.getID()
    grid.addEntity(entity)

    # execute
    entity.setID("new-entity-id")

    # verify
    assert grid.isEntityPresent(entity) == False
    assert grid.getNumEntities() == 1
    assert grid.getEntity(originalID) is entity
    assert grid.getEntity("new-entity-id") == None

def test_grid_removeEntity_after_entity_setID_preserves_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    locationID = entity.getLocationID()
    entity.setID("new-entity-id")

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.getNumEntities() == 1
    assert entity.getGridID() == grid.getID()
    assert entity.getLocationID() == locationID

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

def test_getFirstLocation_of_a_new_grid_is_at_the_origin():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location.getX() == 0
    assert location.getY() == 0

def test_getFirstLocation_after_removing_the_first_is_the_next_in_column_order():
    # prepare
    grid = Grid(RECT_COLUMNS, RECT_ROWS)
    grid.removeLocation(grid.getFirstLocation())

    # execute
    location = grid.getFirstLocation()

    # verify
    assert location.getX() == 0
    assert location.getY() == 1

def test_getFirstLocation_of_an_empty_grid_after_addLocation_is_the_added_location():
    # prepare
    grid = Grid(0, 0)
    location = Location(RECT_COLUMNS, RECT_ROWS)
    grid.addLocation(location)

    # execute
    firstLocation = grid.getFirstLocation()

    # verify
    assert firstLocation is location

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

def test_addLocation_with_an_entity_holds_it_without_setting_its_grid_id():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location.addEntity(entity)

    # execute
    grid.addLocation(location)

    # verify
    assert grid.isEntityPresent(entity) == True
    assert grid.getEntity(entity.getID()) == entity
    assert grid.getNumEntities() == 1
    assert entity.getGridID() == -1
    assert entity.getLocationID() == location.getID()

def test_addLocation_with_an_entity_from_another_grid_preserves_its_grid_id():
    # prepare
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = otherGrid.getRandomLocation()
    otherGrid.addEntityToLocation(entity, location)

    # execute
    grid.addLocation(location)

    # verify
    assert grid.isEntityPresent(entity) == True
    assert otherGrid.isEntityPresent(entity) == True
    assert entity.getGridID() == otherGrid.getID()
    assert entity.getLocationID() == location.getID()

def test_grid_removeEntity_after_addLocation_with_an_entity_clears_containment_ids():
    # prepare
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    location = otherGrid.getRandomLocation()
    otherGrid.addEntityToLocation(entity, location)
    grid.addLocation(location)

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == False
    assert otherGrid.isEntityPresent(entity) == False
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_setLocations_with_a_populated_location_holds_its_entity_without_setting_its_grid_id():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)

    # execute
    grid.setLocations({location.getID(): location})

    # verify
    assert grid.isEntityPresent(entity) == True
    assert grid.getEntity(entity.getID()) == entity
    assert grid.getNumEntities() == 1
    assert entity.getGridID() == -1
    assert entity.getLocationID() == location.getID()

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

def test_getNumEntities_counts_an_entity_once_per_location_that_holds_it():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    locations = list(grid.getLocations().values())
    entity = Entity("test")
    grid.addEntityToLocation(entity, locations[0])
    grid.addEntityToLocation(entity, locations[1])

    # execute
    numEntities = grid.getNumEntities()

    # verify
    assert numEntities == 2

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

# test an entity held by more than one grid
def test_addEntity_to_a_second_grid_leaves_it_in_the_first():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntityToLocation(entity, grid.getRandomLocation())
    otherLocation = otherGrid.getRandomLocation()

    # execute
    otherGrid.addEntityToLocation(entity, otherLocation)

    # verify
    assert grid.isEntityPresent(entity) == True
    assert otherGrid.isEntityPresent(entity) == True
    assert grid.getEntity(entity.getID()) is entity
    assert otherGrid.getEntity(entity.getID()) is entity
    assert entity.getGridID() == otherGrid.getID()
    assert entity.getLocationID() == otherLocation.getID()

def test_grid_removeEntity_from_the_earlier_grid_clears_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntityToLocation(entity, grid.getRandomLocation())
    otherGrid.addEntityToLocation(entity, otherGrid.getRandomLocation())

    # execute
    grid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == False
    assert otherGrid.isEntityPresent(entity) == True
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_grid_removeEntity_from_the_later_grid_clears_containment_ids():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    otherGrid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntityToLocation(entity, grid.getRandomLocation())
    otherGrid.addEntityToLocation(entity, otherGrid.getRandomLocation())

    # execute
    otherGrid.removeEntity(entity)

    # verify
    assert grid.isEntityPresent(entity) == True
    assert otherGrid.isEntityPresent(entity) == False
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

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

# test navigating from a None location
# The directional methods only guard against -1, so None raises (see #58).
@pytest.mark.parametrize("direction", ["getUp", "getRight", "getDown", "getLeft"])
def test_navigating_from_None_raises_attribute_error(direction):
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)

    # execute and verify
    with pytest.raises(AttributeError):
        getattr(grid, direction)(None)

def test_navigating_from_a_missing_location_raises_attribute_error():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    missing = grid.getLocation("missing-location-id")

    # execute and verify
    assert missing is None
    with pytest.raises(AttributeError):
        grid.getUp(missing)

def test_navigating_from_the_random_location_of_an_empty_grid_raises_attribute_error():
    # prepare
    grid = Grid(0, 0)

    # execute and verify
    with pytest.raises(AttributeError):
        grid.getUp(grid.getRandomLocation())

def test_navigating_off_an_edge_and_on_returns_minus_one():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    corner = grid.getLocationByCoordinates(0, 0)

    # execute
    offAndOn = grid.getDown(grid.getUp(corner))

    # verify
    assert offAndOn == -1

@pytest.mark.parametrize("direction", ["getUp", "getRight", "getDown", "getLeft"])
def test_navigating_from_the_only_location_of_a_single_location_grid_returns_minus_one(direction):
    # prepare
    grid = Grid(1, 1)
    location = grid.getFirstLocation()

    # execute
    neighbour = getattr(grid, direction)(location)

    # verify
    assert neighbour == -1

# test locations that share coordinates
def test_addLocation_with_the_coordinates_of_an_existing_location_keeps_both():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    original = grid.getLocationByCoordinates(0, 0)
    duplicate = Location(0, 0)
    sizeBefore = grid.getSize()

    # execute
    grid.addLocation(duplicate)

    # verify
    assert grid.getSize() == sizeBefore + 1
    assert grid.getLocation(original.getID()) is original
    assert grid.getLocation(duplicate.getID()) is duplicate

def test_getLocationByCoordinates_shared_by_two_locations_returns_the_earlier_one():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    original = grid.getLocationByCoordinates(0, 0)
    duplicate = Location(0, 0)

    # execute
    grid.addLocation(duplicate)

    # verify
    assert grid.getLocationByCoordinates(0, 0) is original

def test_getLocationByCoordinates_shared_by_two_locations_returns_the_later_one_once_the_earlier_is_removed():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    original = grid.getLocationByCoordinates(0, 0)
    duplicate = Location(0, 0)
    grid.addLocation(duplicate)

    # execute
    grid.removeLocation(original)

    # verify
    assert grid.getLocationByCoordinates(0, 0) is duplicate

# test the dictionaries that a grid returns and stores
def test_getLocations_returns_the_grids_own_dictionary():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getLocationByCoordinates(0, 0)

    # execute
    del grid.getLocations()[location.getID()]

    # verify
    assert grid.getSize() == NORMAL_SIZE * NORMAL_SIZE - 1
    assert grid.getLocationByCoordinates(0, 0) == -1

def test_setLocations_stores_the_given_dictionary_without_copying_it():
    # prepare
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    locations = dict()
    grid.setLocations(locations)
    location = Location(0, 0)

    # execute
    locations[location.getID()] = location

    # verify
    assert grid.getLocations() is locations
    assert grid.getSize() == 1
    assert grid.getLocationByCoordinates(0, 0) is location

# test the IDs a grid looks up by
def test_getLocations_is_keyed_by_location_uuid():
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    for locationId, location in grid.getLocations().items():
        assert isinstance(locationId, uuid.UUID)
        assert locationId == location.getID()

def test_getLocation_with_the_string_form_of_the_id_returns_None(capsys):
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    location = grid.getFirstLocation()
    capsys.readouterr()

    assert grid.getLocation(str(location.getID())) == None
    assert capsys.readouterr().out == "Warning: A location was not present when attempting to retrieve it from a grid.\n"
    assert grid.getLocation(location.getID()) is location

def test_retrieving_entity_by_the_string_form_of_its_id_returns_None(capsys):
    grid = Grid(NORMAL_SIZE, NORMAL_SIZE)
    entity = Entity("test")
    grid.addEntity(entity)
    capsys.readouterr()

    assert grid.getEntity(str(entity.getID())) == None
    assert capsys.readouterr().out == ""
    assert grid.getEntity(entity.getID()) is entity
