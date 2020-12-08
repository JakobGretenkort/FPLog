DROP DATABASE IF EXISTS fplog;
CREATE DATABASE fplog;

-- Tables

CREATE TABLE fplog.website (
  id_website INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  url TEXT NOT NULL
);

CREATE TABLE fplog.attribute (
  id_attribute INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  object TEXT NOT NULL,
  attribute TEXT NOT NULL,
  UNIQUE(object, attribute)
);

CREATE TABLE fplog.font (
  id_font INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name TEXT NOT NULL
);

CREATE TABLE fplog.accesses (
  id_website INT UNSIGNED,
  id_attribute INT UNSIGNED,
  PRIMARY KEY(id_website, id_attribute)
);

CREATE TABLE fplog.loads (
  id_website INT UNSIGNED,
  id_font INT UNSIGNED,
  PRIMARY KEY(id_website, id_font)
);