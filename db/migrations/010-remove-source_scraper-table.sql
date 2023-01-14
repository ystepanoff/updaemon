DROP TABLE source_scraper;
ALTER TABLE source ADD scraper_id INT NOT NULL REFERENCES scraper(id);
ALTER TABLE source ADD params JSON;
ALTER TABLE scraper ADD params_config JSON;