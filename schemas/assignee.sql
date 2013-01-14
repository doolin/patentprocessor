CREATE TABLE "assignee" (
                Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER);
CREATE TABLE "assignee_1" (
                Patent VARCHAR(8),      AsgType INTEGER,        Assignee VARCHAR(30),
                City VARCHAR(10),       State VARCHAR(2),       Country VARCHAR(2),
                Nationality VARCHAR(2), Residence VARCHAR(2),   AsgSeq INTEGER, assigneeAsc VARCHAR(30), AsgNum INTEGER, NCity, NState, NCountry, NZipcode, NLat, NLong);
CREATE TABLE gXML ( week VARCHAR );
CREATE TABLE grp(
  Mtch,
  assigneeAsc TEXT,
  assigneeAsc2,
  assigneeAsc3,
  Block1,
  Block2,
  Block3,
  AsgNum,
  AsgNum2,
  nFreqS,
  nFreqB,
  cnt
);
CREATE TABLE wrd (
                word TEXT, word1 TEXT, word_N TEXT, count INTEGER, countF INTEGER);
CREATE INDEX B_3c ON grp (Block3, AsgNum2);
CREATE INDEX Bl1 ON grp (Block1);
CREATE INDEX Bl1c ON grp (Block1, AsgNum2);
CREATE INDEX Bl2 ON grp (Block2);
CREATE INDEX Bl2c ON grp (Block2, AsgNum2);
CREATE INDEX Bl3c ON grp (assigneeAsc2, AsgNum2);
CREATE INDEX Bl4c ON grp (assigneeAsc3, AsgNum2);
CREATE INDEX aGaN2 ON grp (AsgNum2);
CREATE UNIQUE INDEX aGasg ON grp (assigneeAsc);
CREATE INDEX aWw  ON wrd (word);
CREATE INDEX aWw3 ON wrd (word1);
CREATE INDEX assignee_1_idx_asg    ON "assignee_1" (Assignee);
CREATE INDEX assignee_1_idx_asgtyp ON "assignee_1" (AsgType);
CREATE INDEX assignee_1_idx_cty ON "assignee_1" (Country);
CREATE INDEX assignee_1_idx_patent ON "assignee_1" (Patent);
CREATE INDEX assignee_1_idx_stt ON "assignee_1" (State);
CREATE UNIQUE INDEX assignee_1_uqAsg ON "assignee_1" (Patent, AsgSeq);
CREATE INDEX idx_asg    ON "assignee" (Assignee);
CREATE INDEX idx_asgtyp ON "assignee" (AsgType);
CREATE INDEX idx_cty ON "assignee" (Country);
CREATE INDEX idx_patent ON "assignee" (Patent);
CREATE INDEX idx_stt ON "assignee" (State);
CREATE UNIQUE INDEX uqAsg ON "assignee" (Patent, AsgSeq);
