from unittest.mock import MagicMock
from src.entity import Entity

# test initializing entity
def test_initialization():
    entity = Entity("test")
    assert entity.id != None
    assert entity.name == "test"
    assert entity.creationDate != None
    assert entity.environmentID == -1
    assert entity.gridID == -1
    assert entity.locationID == -1

# test getters
def test_getters():
    entity = Entity("test")
    assert entity.getID() != None
    assert entity.getName() == "test"
    assert entity.getEnvironmentID() == -1
    assert entity.getCreationDate() != None
    assert entity.getGridID() == -1
    assert entity.getLocationID() == -1

# test setters
def test_setters():
    entity = Entity("test")
    entity.setID(1)
    assert entity.getID() == 1
    entity.setName("test2")
    assert entity.getName() == "test2"
    entity.setEnvironmentID(2)
    assert entity.getEnvironmentID() == 2
    entity.setCreationDate("test3")
    assert entity.getCreationDate() == "test3"
    entity.setGridID(3)
    assert entity.getGridID() == 3
    entity.setLocationID(4)
    assert entity.getLocationID() == 4

# test printing info
def test_printInfo():
    entity = Entity("test")
    entity.printInfo = MagicMock()
    entity.printInfo()
    entity.printInfo.assert_called_once_with()

def test_printInfo_output(capsys):
    # prepare
    entity = Entity("test")
    entity.setID(1)
    entity.setCreationDate("date")
    entity.setEnvironmentID(2)
    entity.setGridID(3)
    entity.setLocationID(4)

    # execute
    entity.printInfo()

    # verify
    assert capsys.readouterr().out == (
        "--------------\n"
        "test\n"
        "--------------\n"
        "ID:  1\n"
        "Creation Date:  date\n"
        "Environment ID:  2\n"
        "Grid ID:  3\n"
        "Location ID:  4\n"
        "\n\n"
    )

def test_printInfo_output_for_an_uncontained_entity(capsys):
    # prepare
    entity = Entity("test")
    entity.setID(1)
    entity.setCreationDate("date")

    # execute
    entity.printInfo()

    # verify
    output = capsys.readouterr().out
    assert "Environment ID:  -1\n" in output
    assert "Grid ID:  -1\n" in output
    assert "Location ID:  -1\n" in output