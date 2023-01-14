DROP TABLE source_action;
CREATE TABLE source_action (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    source_id INT NOT NULL REFERENCES source(id),
    action_id INT NOT NULL REFERENCES action(id),
    params JSON
);