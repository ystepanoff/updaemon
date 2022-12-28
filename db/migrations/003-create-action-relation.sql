CREATE TABLE action (
    id INT NOT NULL AUTO_INCREMENT,
    base_class VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE source_action (
    source_id INT NOT NULL,
    action_id INT NOT NULL,
    params JSON,
    FOREIGN KEY (source_id) REFERENCES source(id),
    FOREIGN KEY (action_id) REFERENCES action(id)
)