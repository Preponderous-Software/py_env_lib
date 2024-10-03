-- Copyright (c) 2024 Preponderous Software
-- MIT License

-- drop all tables
DROP TABLE IF EXISTS entity CASCADE;
DROP TABLE IF EXISTS location CASCADE;
DROP TABLE IF EXISTS grid CASCADE;
DROP TABLE IF EXISTS environment CASCADE;
DROP TABLE IF EXISTS entity_location CASCADE;

DROP TABLE IF EXISTS location_grid CASCADE;
DROP TABLE IF EXISTS grid_environment CASCADE;

DROP TABLE IF EXISTS entity_grid CASCADE;
DROP TABLE IF EXISTS entity_environment CASCADE;
DROP TABLE IF EXISTS location_environment CASCADE;