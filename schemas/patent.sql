/**
 * TODO: Document appropriately.
 * Patent  VARCHAR(8),
 * Kind    VARCHAR(3),
 * Claims  INTEGER,
 * AppType INTEGER,
 * AppNum  VARCHAR(8),
 * GDate   INTEGER,
 * GYear   INTEGER,
 * AppDate INTEGER,
 * AppYear INTEGER,
 * PatType VARCHAR(15)
 */

-- TODO: Pluralize table name
-- TODO: Lowercase column names
-- TODO: Underscore appropriately
CREATE TABLE patent (
  Patent VARCHAR(8),
  Kind VARCHAR(3),
  Claims INTEGER,
  AppType INTEGER,
  AppNum VARCHAR(8),
  GDate INTEGER,
  GYear INTEGER,
  AppDate INTEGER,
  AppYear INTEGER,
  PatType VARCHAR(15)
);


CREATE INDEX idx_ayr      ON patent (AppYear);
CREATE INDEX idx_gyr      ON patent (GYear);
CREATE INDEX idx_patent   ON patent (Patent);
CREATE UNIQUE INDEX uqPat ON patent (Patent);

-- TODO: Add example XML snippet
