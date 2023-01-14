ALTER TABLE source_action DROP source_id;
ALTER TABLE source_action DROP action_id;
ALTER TABLE source_action ADD source_id INT NOT NULL REFERENCES source(id) ON DELETE CASCADE FIRST;
ALTER TABLE source_action ADD action_id INT NOT NULL REFERENCES action(id) ON DELETE CASCADE AFTER source_id;
ALTER TABLE source DROP scraper_id;
ALTER TABLE source ADD scraper_id INT NOT NULL REFERENCES scraper(id) ON DELETE CASCADE AFTER remote;
DROP TABLE state;
CREATE TABLE state (
    source_id INT NOT NULL REFERENCES source(id) ON DELETE CASCADE ,
    data TEXT,
    updated_at DATETIME
);