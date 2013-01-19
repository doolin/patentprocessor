/**
 * TODO: Document appropriately
 * Patent:
 * Firstname:
 * Lastname:
 * Street:
 * City:
 * State:
 * Country:
 * Zipcode:
 * Nationality:
 * InvSeq:
 */

-- TODO: Remove quote from "inventor"
-- TODO: Lower case column names
-- TODO: Pluralize table name to tables
-- TODO: Underscore separate InvSeq
CREATE TABLE "inventor" (
  Patent      VARCHAR(8),
  Firstname   VARCHAR(15),
  Lastname    VARCHAR(15),
  Street      VARCHAR(15),
  City        VARCHAR(10),
  State       VARCHAR(2),
  Country     VARCHAR(12),
  Zipcode     VARCHAR(5),
  Nationality VARCHAR(2),
  InvSeq      INTEGER
);


CREATE INDEX idx_cty      ON "inventor" (Country);
CREATE INDEX idx_patent   ON "inventor" (Patent);
CREATE INDEX idx_stt      ON "inventor" (State);
CREATE UNIQUE INDEX uqInv ON "inventor" (Patent, InvSeq);
