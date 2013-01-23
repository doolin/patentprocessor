/**
 * TODO: Document appropriately
 * Patent   VARCHAR(8),
 * Abstract VARCHAR(50),
 * Title    VARCHAR(20)
 */

-- TODO: Pluralize table name
-- TODO: Lowercase columns
CREATE TABLE patdesc (
  Patent   VARCHAR(8),
  Abstract VARCHAR(50),
  Title    VARCHAR(20)
);

-- TODO: rename indexes appropriately.
CREATE INDEX idx_patent ON patdesc (Patent);
CREATE UNIQUE INDEX uqPatDesc ON patdesc (Patent);

-- TODO: Add example XML snippet
