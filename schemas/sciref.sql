/**
 * TODO: Document appropriately
 * Patent  VARCHAR(8),
 * Descrip VARCHAR(20),
 * CitSeq  INTEGER
 */


-- TODO: Pluralize table name
-- TODO: Underscore appropriately
-- TODO: Lowercase column names
CREATE TABLE sciref (
  Patent  VARCHAR(8),
  Descrip VARCHAR(20),
  CitSeq  INTEGER
);


-- TODO: rename indexes appropriately.
CREATE INDEX idx_patent      ON sciref (Patent);
CREATE UNIQUE INDEX uqSciref ON sciref (Patent, CitSeq);

-- TODO: Add example XML snippet
