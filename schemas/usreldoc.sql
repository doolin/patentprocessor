CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE usreldoc (
                Patent VARCHAR(8),      DocType VARCHAR(10),    OrderSeq INTEGER,
                Country VARCHAR(2),     RelPatent VARCHAR(8),   Kind VARCHAR(2),
                RelDate INTEGER,        Status VARCHAR(10));
CREATE INDEX idx_patent ON usreldoc (Patent);
CREATE INDEX idx_relpat ON usreldoc (RelPatent);
CREATE UNIQUE INDEX uqUSRelDoc ON usreldoc (Patent, OrderSeq);
