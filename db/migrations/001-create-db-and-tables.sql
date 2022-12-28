CREATE TABLE migrations (
    id INT NOT NULL,
    name VARCHAR(255),
    PRIMARY KEY(id)
);

CREATE TABLE source (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(256),
    description TEXT,
    type VARCHAR(255),
    remote VARCHAR(255),
    PRIMARY KEY(id),
    UNIQUE KEY(name)
);