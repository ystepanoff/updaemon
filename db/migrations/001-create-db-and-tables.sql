CREATE TABLE migrations (
    id INT NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE source (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256),
    description TEXT,
    params JSON,
    PRIMARY KEY(id),
    UNIQUE KEY(name)
);