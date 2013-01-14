CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE "inventor" (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                Street VARCHAR(15),     City VARCHAR(10),
                State VARCHAR(2),       Country VARCHAR(12),
                Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER);
CREATE TABLE "inventor_1" (
                Patent VARCHAR(8),      Firstname VARCHAR(15),  Lastname VARCHAR(15),
                Street VARCHAR(15),     City VARCHAR(10),
                State VARCHAR(2),       Country VARCHAR(12),
                Zipcode VARCHAR(5),     Nationality VARCHAR(2), InvSeq INTEGER, NCity, NState, NCountry, NZipcode, NLat, NLong);
CREATE INDEX idx_cty ON "inventor" (Country);
CREATE INDEX idx_patent ON "inventor" (Patent);
CREATE INDEX idx_stt ON "inventor" (State);
CREATE INDEX inventor_1_idx_cty ON "inventor_1" (Country);
CREATE INDEX inventor_1_idx_patent ON "inventor_1" (Patent);
CREATE INDEX inventor_1_idx_stt ON "inventor_1" (State);
CREATE UNIQUE INDEX inventor_1_uqInv ON "inventor_1" (Patent, InvSeq);
CREATE UNIQUE INDEX uqInv ON "inventor" (Patent, InvSeq);
