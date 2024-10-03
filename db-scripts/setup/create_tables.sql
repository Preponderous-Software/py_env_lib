-- Copyright (c) 2024 Preponderous Software
-- MIT License

-- entity table (entity_id, name, creationDate)
CREATE TABLE entity (
    entity_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creationDate TIMESTAMP NOT NULL
);

-- location table (location_id, x, y)
CREATE TABLE location (
    location_id INT PRIMARY KEY,
    x INT NOT NULL,
    y INT NOT NULL
);

-- grid table (grid_id, columns, rows)
CREATE TABLE grid (
    grid_id INT PRIMARY KEY,
    columns INT NOT NULL,
    rows INT NOT NULL
);

-- environment table (environment_id, name, creationDate)
CREATE TABLE environment (
    environment_id INT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creationDate TIMESTAMP NOT NULL
);

-- entity_location table (entity_id, location_id)
CREATE TABLE entity_location (
    entity_id INT NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY (entity_id, location_id),
    FOREIGN KEY (entity_id) REFERENCES entity(entity_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- location_grid table (grid_id, location_id)
CREATE TABLE location_grid (
    grid_id INT NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY (grid_id, location_id),
    FOREIGN KEY (grid_id) REFERENCES grid(grid_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- location_environment table (environment_id, location_id)
CREATE TABLE location_environment (
    environment_id INT NOT NULL,
    location_id INT NOT NULL,
    PRIMARY KEY (environment_id, location_id),
    FOREIGN KEY (environment_id) REFERENCES environment(environment_id),
    FOREIGN KEY (location_id) REFERENCES location(location_id)
);

-- entity_grid table (entity_id, grid_id)
CREATE TABLE entity_grid (
    entity_id INT NOT NULL,
    grid_id INT NOT NULL,
    PRIMARY KEY (entity_id, grid_id),
    FOREIGN KEY (entity_id) REFERENCES entity(entity_id),
    FOREIGN KEY (grid_id) REFERENCES grid(grid_id)
);

-- grid_environment table (environment_id, grid_id)
CREATE TABLE grid_environment (
    environment_id INT NOT NULL,
    grid_id INT NOT NULL,
    PRIMARY KEY (environment_id, grid_id),
    FOREIGN KEY (environment_id) REFERENCES environment(environment_id),
    FOREIGN KEY (grid_id) REFERENCES grid(grid_id)
);


-- entity_environment table (entity_id, environment_id)
CREATE TABLE entity_environment (
    entity_id INT NOT NULL,
    environment_id INT NOT NULL,
    PRIMARY KEY (entity_id, environment_id),
    FOREIGN KEY (entity_id) REFERENCES entity(entity_id),
    FOREIGN KEY (environment_id) REFERENCES environment(environment_id)
);