-- Copyright (c) 2024 Preponderous Software
-- MIT License

-- create environment, grid and location data
INSERT INTO environment (environment_id, name, creationDate) VALUES (1, 'Test Environment', '2024-01-01 00:00:00');
INSERT INTO grid (grid_id, columns, rows) VALUES (1, 4, 4);
INSERT INTO location (location_id, x, y) VALUES (1, 0, 0);
INSERT INTO location (location_id, x, y) VALUES (2, 1, 0);
INSERT INTO location (location_id, x, y) VALUES (3, 2, 0);
INSERT INTO location (location_id, x, y) VALUES (4, 3, 0);
INSERT INTO location (location_id, x, y) VALUES (5, 0, 1);
INSERT INTO location (location_id, x, y) VALUES (6, 1, 1);
INSERT INTO location (location_id, x, y) VALUES (7, 2, 1);
INSERT INTO location (location_id, x, y) VALUES (8, 3, 1);
INSERT INTO location (location_id, x, y) VALUES (9, 0, 2);
INSERT INTO location (location_id, x, y) VALUES (10, 1, 2);
INSERT INTO location (location_id, x, y) VALUES (11, 2, 2);
INSERT INTO location (location_id, x, y) VALUES (12, 3, 2);
INSERT INTO location (location_id, x, y) VALUES (13, 0, 3);
INSERT INTO location (location_id, x, y) VALUES (14, 1, 3);
INSERT INTO location (location_id, x, y) VALUES (15, 2, 3);
INSERT INTO location (location_id, x, y) VALUES (16, 3, 3);

-- create entities
INSERT INTO entity (entity_id, name) VALUES (1, 'Dave the Cat');
INSERT INTO entity (entity_id, name) VALUES (2, 'Sally the Dog');
INSERT INTO entity (entity_id, name) VALUES (3, 'Bob the Fish');
INSERT INTO entity (entity_id, name) VALUES (4, 'Alice the Bird');

-- associate locations with grid
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 1);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 2);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 3);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 4);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 5);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 6);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 7);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 8);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 9);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 10);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 11);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 12);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 13);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 14);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 15);
INSERT INTO location_grid (grid_id, location_id) VALUES (1, 16);

-- associate locations with environment
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 1);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 2);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 3);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 4);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 5);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 6);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 7);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 8);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 9);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 10);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 11);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 12);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 13);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 14);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 15);
INSERT INTO location_environment (environment_id, location_id) VALUES (1, 16);

-- associate grid with environment
INSERT INTO grid_environment (grid_id, environment_id) VALUES (1, 1);

-- associate entities with locations
INSERT INTO entity_location (entity_id, location_id) VALUES (1, 1);
INSERT INTO entity_location (entity_id, location_id) VALUES (2, 2);
INSERT INTO entity_location (entity_id, location_id) VALUES (3, 3);
INSERT INTO entity_location (entity_id, location_id) VALUES (4, 4);

-- associate entities with grid
INSERT INTO entity_grid (entity_id, grid_id) VALUES (1, 1);
INSERT INTO entity_grid (entity_id, grid_id) VALUES (2, 1);
INSERT INTO entity_grid (entity_id, grid_id) VALUES (3, 1);
INSERT INTO entity_grid (entity_id, grid_id) VALUES (4, 1);

-- associate entities with environment
INSERT INTO entity_environment (entity_id, environment_id) VALUES (1, 1);
INSERT INTO entity_environment (entity_id, environment_id) VALUES (2, 1);
INSERT INTO entity_environment (entity_id, environment_id) VALUES (3, 1);
INSERT INTO entity_environment (entity_id, environment_id) VALUES (4, 1);