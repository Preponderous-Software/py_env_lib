from unittest.mock import MagicMock
from src.location import Location
from src.entity import Entity

# test initializing location
def test_initialization():
    location = Location(0, 0)
    assert location.id != None
    assert location.x == 0
    assert location.y == 0

# test getters
def test_getters():
    location = Location(0, 0)
    assert location.getID() != None
    assert location.getX() == 0
    assert location.getY() == 0

# test getting number of entities
def test_getNumEntities():
    location = Location(0, 0)
    assert location.getNumEntities() == 0

# test adding entity
def test_addEntity(monkeypatch):
    isEntityPresent = MagicMock(return_value=False)
    setLocationID = MagicMock()
    monkeypatch.setattr(Location, "isEntityPresent", isEntityPresent)
    monkeypatch.setattr(Entity, "setLocationID", setLocationID)

    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert location.getNumEntities() == 1

    # test that isEntityPresent was called
    isEntityPresent.assert_called_once_with(entity)

    # test that setLocationID was called
    setLocationID.assert_called_once_with(location.getID())

# test removing entity
def test_removeEntity(monkeypatch):
    setLocationID = MagicMock()
    monkeypatch.setattr(Location, "isEntityPresent", MagicMock(return_value=False))
    monkeypatch.setattr(Entity, "setLocationID", setLocationID)

    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)

    isEntityPresent = MagicMock(return_value=True)
    monkeypatch.setattr(Location, "isEntityPresent", isEntityPresent)
    location.removeEntity(entity)
    assert location.getNumEntities() == 0

    # test that isEntityPresent was called
    isEntityPresent.assert_called_once_with(entity)

    # test that setLocationID was called
    setLocationID.assert_called()

def test_removeEntity_clears_location_id():
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert entity.getLocationID() == location.getID()

    location.removeEntity(entity)
    assert entity.getLocationID() == -1

def test_removeEntity_not_present_preserves_location_id():
    occupiedLocation = Location(0, 0)
    otherLocation = Location(1, 1)
    entity = Entity("test")
    occupiedLocation.addEntity(entity)

    otherLocation.removeEntity(entity)
    assert entity.getLocationID() == occupiedLocation.getID()

# test checking if entity is present
def test_isEntityPresent():
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert location.getNumEntities() == 1
    assert location.isEntityPresent(entity) == True

def test_isEntityPresent_not_present():
    location = Location(0, 0)
    entity = Entity("test")
    assert location.isEntityPresent(entity) == False

# test getting entities
def test_getEntities(monkeypatch):
    monkeypatch.setattr(Location, "isEntityPresent", MagicMock(return_value=False))
    monkeypatch.setattr(Entity, "setLocationID", MagicMock())

    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    assert len(location.getEntities()) == 1

def test_getEntityById():
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    retrievedEntity = location.getEntity(entity.getID())
    assert retrievedEntity == entity

def test_getEntityById_not_present():
    location = Location(0, 0)
    entity = Entity("test")
    retrievedEntity = location.getEntity(entity.getID())
    assert retrievedEntity == None

def test_getEntityById_not_present_warns(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    capsys.readouterr()

    location.getEntity(entity.getID())
    assert capsys.readouterr().out == "Warning: An entity was not present when attempting to retrieve it from a location.\n"

def test_getEntityById_is_silent(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    capsys.readouterr()

    location.getEntity(entity.getID())
    assert capsys.readouterr().out == ""

# test warnings when adding and removing entities
def test_addEntity_already_present_is_not_duplicated():
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)

    location.addEntity(entity)
    assert location.getNumEntities() == 1
    assert entity.getLocationID() == location.getID()

def test_addEntity_already_present_warns(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    capsys.readouterr()

    location.addEntity(entity)
    assert capsys.readouterr().out == "Warning: An entity was already present when attempting to add it to a location.\n"

def test_addEntity_is_silent(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    capsys.readouterr()

    location.addEntity(entity)
    assert capsys.readouterr().out == ""

def test_removeEntity_not_present_warns(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    capsys.readouterr()

    location.removeEntity(entity)
    assert capsys.readouterr().out == "Warning: An entity was not present when attempting to remove it from a location.\n"

def test_removeEntity_is_silent(capsys):
    location = Location(0, 0)
    entity = Entity("test")
    location.addEntity(entity)
    capsys.readouterr()

    location.removeEntity(entity)
    assert capsys.readouterr().out == ""