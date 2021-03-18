DROP DATABASE IF EXISTS fplog;
CREATE DATABASE fplog;

-- Tables

CREATE TABLE fplog.url (
  time INT NOT NULL,
  url VARCHAR(8192) NOT NULL,
  parent VARCHAR(8192)
);

CREATE TABLE fplog.access (
  time INT NOT NULL,
  url VARCHAR(8192) NOT NULL,
  parent VARCHAR(8192),
  top VARCHAR(8192) NOT NULL,
  object VARCHAR(255) NOT NULL,
  accessed VARCHAR(255) NOT NULL,
  parameters VARCHAR(255)
);

CREATE TABLE fplog.font (
  time INT NOT NULL,
  url VARCHAR(8192) NOT NULL,
  parent VARCHAR(8192),
  top VARCHAR(8192) NOT NULL,
  fontname VARCHAR(255) NOT NULL,
  priority INT NOT NULL
);

CREATE TABLE fplog.surface_group (
  name INT NOT NULL,
  max REAL NOT NULL
);

-- Drop duplicates (tested with postgres)

-- This one is not actually used
DELETE FROM fplog.url a
  USING fplog.url b
WHERE a.ctid > b.ctid
  AND a.url = b.url
  AND a.parent = b.parent;

DELETE FROM fplog.access a
  USING fplog.access b
WHERE a.ctid > b.ctid
  AND a.url = b.url
  AND a.parent = b.parent
  AND a.top = b.top
  AND a.object = b.object
  AND a.accessed = b.accessed
  AND a.parameters = b.parameters;

DELETE FROM fplog.font a
  USING fplog.font b
WHERE a.ctid > b.ctid
  AND a.url = b.url
  AND a.parent = b.parent
  AND a.top = b.top
  AND a.fontname = b.fontname
  AND a.priority = b.priority;