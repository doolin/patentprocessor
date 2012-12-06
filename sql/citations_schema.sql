
/** Citations in the SQLite3 files are
 * split. This table covers years 2000
 * through 2010. Schemas for other years
 * are identical.
 */
CREATE TABLE citation00_10 (
  Patent      VARCHAR(8),
  Cit_Date    INTEGER,
  Cit_Name    VARCHAR(10),
  Cit_Kind    VARCHAR(1),
  Cit_Country VARCHAR(2),
  Citation    VARCHAR(8),
  Category    VARCHAR(15),
  CitSeq      INTEGER);


CREATE UNIQUE INDEX idx_idx1 ON citation00_10 (patent,citation);
CREATE INDEX idx_idx2 ON citation00_10 (citation);
CREATE INDEX idx_idx3 ON citation00_10 (patent);
