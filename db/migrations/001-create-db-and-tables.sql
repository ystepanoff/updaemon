CREATE DATABASE updaemon;
USE updaemon;
CREATE TABLE migrations (id INT NOT NULL, name VARCHAR(255), primary key (id));
CREATE TABLE source (id INT NOT NULL AUTO_INCREMENT, name VARCHAR(255), description TEXT, params JSON);
