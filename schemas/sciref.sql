CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE sciref (
                Patent VARCHAR(8),      Descrip VARCHAR(20),    CitSeq INTEGER);
CREATE INDEX idx_patent ON sciref (Patent);
CREATE UNIQUE INDEX uqSciref ON sciref (Patent, CitSeq);
