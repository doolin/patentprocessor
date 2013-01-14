CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE lawyer (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                LawCountry VARCHAR(2),  OrgName VARCHAR(20),    LawSeq INTEGER);
CREATE INDEX idx_patent ON lawyer (Patent);
CREATE INDEX idx_patl ON lawyer (Patent, LawSeq);
CREATE UNIQUE INDEX uqLawyer ON lawyer (Patent, LawSeq);
