# py_env_lib
This python library provides base classes for creating 2D virtual worlds.

## Classes
Name | Description
----- | -----
Entity | Represents an entity that can exist in a location.
Environment | Represents a virtual environment with an underlying 2D grid of locations that can contain entities.
Grid | Represents a grid of locations.
Location | Represents a location that can contain entities.

Entities exist in locations. Locations exist in grids. Grids exist in environments. Environments serve as the interface for developers to affect the locations and entities within.

## Usage
This library is not published as a package. Modules are imported from `src`, so the repository root must be on the Python path, for example by setting `PYTHONPATH` to it.

```python
from src.entity import Entity
from src.environment import Environment

# An environment of size 3 has a 3x3 grid of locations.
environment = Environment("Example", 3)
grid = environment.getGrid()

# Without a location, an entity is placed in a random one.
wanderer = Entity("Wanderer")
environment.addEntity(wanderer)
print(grid.getLocation(wanderer.getLocationID()).getNumEntities())  # 1

# An entity can also be placed in a specific location.
settler = Entity("Settler")
center = grid.getLocationByCoordinates(1, 1)
environment.addEntityToLocation(settler, center)
print(settler.getLocationID() == center.getID())  # True

# Locations can be navigated from one to the next.
print(grid.getRight(center).getX())  # 2

environment.removeEntity(wanderer)
environment.removeEntity(settler)
print(environment.getNumEntities())  # 0
```

Not every lookup signals "not found" the same way. `getLocationByCoordinates`, `getUp`, `getRight`, `getDown` and `getLeft` return `-1`, while `getLocation`, `getFirstLocation`, `getRandomLocation` and `getEntity` return `None`.

## Containment IDs
An entity records where it is held through `getEnvironmentID`, `getGridID` and `getLocationID`, each of which returns `-1` when nothing is recorded. Each level only maintains its own ID and those below it. `addEntityToLocation` sets the same IDs as `addEntity`:

Called on | `addEntity` sets | `removeEntity` clears
----- | ----- | -----
`Environment` | environment, grid and location IDs | environment, grid and location IDs
`Grid` | grid and location IDs | grid and location IDs
`Location` | location ID | location ID

An entity added to an environment should therefore be removed through that environment. Removing it through its grid or location takes it out of the environment but leaves the higher-level IDs set.

The IDs are not kept in step with the following operations. Whether this should change is an open question, so these describe current behaviour rather than a guarantee:

- `Grid.removeLocation` and `Grid.setLocations` leave the IDs of the entities in the discarded locations unchanged ([#69](https://github.com/Preponderous-Software/py_env_lib/issues/69)).
- `Grid.addLocation` and `Grid.setLocations` do not set the grid ID of the entities already in the locations they add. The grid then holds those entities, and `Grid.removeEntity` still clears their grid and location IDs.
- `Environment.setGrid` leaves the entities in the replaced grid, with their IDs unchanged. `Environment.removeEntity` then has no effect on them ([#78](https://github.com/Preponderous-Software/py_env_lib/issues/78)).
- Adding an entity to a second location or environment does not remove it from the first, and both then hold it. Its IDs name the latest one, and removing it from the earlier one still clears the IDs listed in the table above, even though the later one holds it ([#70](https://github.com/Preponderous-Software/py_env_lib/issues/70)).
- `Entity.setID` does not re-key an entity that is already held. It stays stored under its previous ID, so `isEntityPresent` returns `False` and `removeEntity` cannot remove it ([#77](https://github.com/Preponderous-Software/py_env_lib/issues/77)).

## Running the tests
The tests require [pytest](https://docs.pytest.org/). Run them from the repository root:

```bash
bash run_unit_tests.sh
```

## EnvironmentLib
This project is based on EnvironmentLib, which has since been renamed to Viron. The repository can be found [here](https://github.com/Preponderous-Software/viron).

## 📄 License

py_env_lib is licensed under the [MIT License](LICENSE).

Copyright © 2022–2025 Daniel McCoy Stephenson. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the “Software”), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE 
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

---

### Why MIT?
The **MIT License** is simple and highly permissive, removing barriers for individuals, academia, and commercial users to adopt, integrate, and extend **py_env_lib**. This encourages ecosystem growth, increases visibility, and aligns with the goal of making **py_env_lib** a widely used foundation for 2D virtual-world development.

### Open Source Commitment
There are **no plans to move away from open source** for **py_env_lib**. It will remain freely available under an OSI-approved license, with community contributions encouraged and welcomed.
