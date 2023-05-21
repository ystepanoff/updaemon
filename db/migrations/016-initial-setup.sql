DELETE FROM source_action;
DELETE FROM state;
DELETE FROM source;
DELETE FROM action;
DELETE FROM scraper;

INSERT INTO scraper (base_class, params_config, params_order) VALUES ('DummyScraper', '{}', '[]');
INSERT INTO scraper (base_class, params_config, params_order) VALUES ('SimpleHTMLScraper', '{"tag": "str", "attrs": "dict"}', '[]');
INSERT INTO action (base_class, params_config, params_order) VALUES ('DefaultEmailAction', '{"recipients": "list"}', '["recipients"]');
