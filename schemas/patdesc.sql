CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE patdesc (
                Patent VARCHAR(8),
                Abstract VARCHAR(50),   Title VARCHAR(20));
CREATE INDEX idx_patent ON patdesc (Patent);
CREATE UNIQUE INDEX uqPatDesc ON patdesc (Patent);
