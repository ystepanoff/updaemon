CREATE TABLE scraper (
    id INT NOT NULL AUTO_INCREMENT,
    base_class VARCHAR(255),
    PRIMARY KEY (id)
);

CREATE TABLE source_scraper (
    source_id INT NOT NULL UNIQUE,
    scraper_id INT NOT NULL,
    params JSON,
    FOREIGN KEY (source_id) REFERENCES source(id),
    FOREIGN KEY (scraper_id) REFERENCES scraper(id)
);