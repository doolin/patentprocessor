/**
 * TODO: Document appropriately
 * Patent:
 * AsgType:
 * Assignee:
 * City:
 * State:
 * Country:
 * Nationality:
 * Residence:
 * AsgSeq:
 */

-- TODO: Remove quotes from "assignee"
-- TODO: Change table name to assignees
-- TODO: Lower case all column names
-- TODO: Underscore separate column names as appropriate
CREATE TABLE "assignee" (
  Patent      VARCHAR(8),
  AsgType     INTEGER,
  Assignee    VARCHAR(30),
  City        VARCHAR(10),
  State       VARCHAR(2),
  Country     VARCHAR(2),
  Nationality VARCHAR(2),
  Residence   VARCHAR(2),
  AsgSeq      INTEGER
);


-- TODO: Rename indexes appropriately.
CREATE INDEX idx_asg      ON "assignee" (Assignee);
CREATE INDEX idx_asgtyp   ON "assignee" (AsgType);
CREATE INDEX idx_cty      ON "assignee" (Country);
CREATE INDEX idx_patent   ON "assignee" (Patent);
CREATE INDEX idx_stt      ON "assignee" (State);
CREATE UNIQUE INDEX uqAsg ON "assignee" (Patent, AsgSeq);
