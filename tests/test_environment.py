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

# test adding entities
def test_addEntity_sets_containment_ids():
    # prepare
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")

    # execute
    environment.addEntity(entity)

    # verify
    assert environment.isEntityPresent(entity) == True
    assert entity.getEnvironmentID() == environment.getID()
    assert entity.getGridID() == environment.getGrid().getID()

def test_addEntity_to_an_environment_with_no_locations_preserves_containment_ids():
    # prepare
    environment = Environment("empty", 0)
    entity = Entity("test")

    # execute
    environment.addEntity(entity)

    # verify
    assert environment.isEntityPresent(entity) == False
    assert environment.getNumEntities() == 0
    assert entity.getEnvironmentID() == -1
    assert entity.getGridID() == -1

def test_addEntityToLocation_sets_containment_ids():
    # prepare
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    location = environment.getGrid().getFirstLocation()

    # execute
    environment.addEntityToLocation(entity, location)

    # verify
    assert environment.isEntityPresent(entity) == True
    assert entity.getEnvironmentID() == environment.getID()
    assert entity.getGridID() == environment.getGrid().getID()
    assert entity.getLocationID() == location.getID()

def test_addEntityToLocation_not_in_grid_preserves_containment_ids():
    # prepare
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    location = Location(NORMAL_SIZE + 1, NORMAL_SIZE + 1)

    # execute
    environment.addEntityToLocation(entity, location)

    # verify
    assert environment.isEntityPresent(entity) == False
    assert entity.getEnvironmentID() == -1
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

# test removing entities
def test_removeEntity_clears_containment_ids():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    environment.addEntity(entity)
    assert entity.getEnvironmentID() == environment.getID()

    environment.removeEntity(entity)
    assert environment.isEntityPresent(entity) == False
    assert entity.getEnvironmentID() == -1
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

def test_removeEntity_not_present_preserves_containment_ids():
    occupiedEnvironment = Environment("test", NORMAL_SIZE)
    otherEnvironment = Environment("other test", NORMAL_SIZE)
    entity = Entity("test")
    occupiedEnvironment.addEntity(entity)

    otherEnvironment.removeEntity(entity)
    assert occupiedEnvironment.isEntityPresent(entity) == True
    assert entity.getEnvironmentID() == occupiedEnvironment.getID()
    assert entity.getGridID() == occupiedEnvironment.getGrid().getID()

def test_getting_entity_by_id():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    environment.addEntity(entity)
    assert environment.getEntity(entity.getID()) == entity

def test_getting_entity_by_id_not_present():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    assert environment.getEntity(entity.getID()) == None

# test counting entities
def test_getNumEntities_counts_added_entities():
    environment = Environment("test", NORMAL_SIZE)
    for i in range(3):
        environment.addEntity(Entity("test" + str(i)))
    assert environment.getNumEntities() == 3

def test_getNumEntities_after_removing_an_entity():
    environment = Environment("test", NORMAL_SIZE)
    entity = Entity("test")
    otherEntity = Entity("other test")
    environment.addEntity(entity)
    environment.addEntity(otherEntity)

    environment.removeEntity(entity)
    assert environment.getNumEntities() == 1

def test_getNumEntities_delegates_to_grid():
    environment = Environment("test", NORMAL_SIZE)
    grid = MagicMock()
    grid.getNumEntities.return_value = 7
    environment.setGrid(grid)
    assert environment.getNumEntities() == 7
    grid.getNumEntities.assert_called_once_with()

# test printing info
def test_printInfo_output(capsys):
    # prepare
    environment = Environment("test", NORMAL_SIZE)
    environment.setID(1)
    environment.creationDate = "date"
    grid = MagicMock()
    grid.getNumEntities.return_value = 2
    grid.getSize.return_value = 100
    grid.getID.return_value = 3
    environment.setGrid(grid)

    # execute
    environment.printInfo()

    # verify
    assert capsys.readouterr().out == (
        "--------------\n"
        "test\n"
        "--------------\n"
        "Num entities:  2\n"
        "Num locations:  100\n"
        "Creation Date:  date\n"
        "ID:  1\n"
        "Grid ID:  3\n"
        "\n\n"
    )

def test_printInfo_output_reflects_a_real_grid(capsys):
    # prepare
    environment = Environment("test", NORMAL_SIZE)
    environment.addEntity(Entity("test"))

    # execute
    environment.printInfo()

    # verify
    output = capsys.readouterr().out
    assert "Num entities:  1\n" in output
    assert "Num locations:  " + str(NORMAL_SIZE * NORMAL_SIZE) + "\n" in output
    assert "Grid ID:  " + str(environment.getGrid().getID()) + "\n" in output
