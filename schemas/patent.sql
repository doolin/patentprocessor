CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE patent (
                Patent VARCHAR(8),      Kind VARCHAR(3),        Claims INTEGER,
                AppType INTEGER,        AppNum VARCHAR(8),
                GDate INTEGER,          GYear INTEGER,
                AppDate INTEGER,        AppYear INTEGER, PatType VARCHAR(15) );
CREATE INDEX idx_ayr ON patent (AppYear);
CREATE INDEX idx_gyr ON patent (GYear);
CREATE INDEX idx_patent ON patent (Patent);
CREATE UNIQUE INDEX uqPat on patent (Patent);
