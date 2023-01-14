DROP TABLE state;
CREATE TABLE state (
    source_id INT NOT NULL UNIQUE,
    data TEXT,
    updated_at DATETIME,
    FOREIGN KEY (source_id) REFERENCES source(id)
);