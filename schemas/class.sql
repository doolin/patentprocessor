CREATE TABLE class (
                Patent VARCHAR(8),      Prim INTEGER,
                Class VARCHAR(3),       SubClass VARCHAR(3));
CREATE TABLE gXML ( week VARCHAR );
CREATE INDEX idx_cls  ON class (Class);
CREATE INDEX idx_cscl ON class (Class,SubClass);
CREATE INDEX idx_patent ON class (Patent);
CREATE INDEX idx_prim ON class (Prim);
CREATE INDEX idx_scls ON class (SubClass);
CREATE UNIQUE INDEX uqClass ON class (Patent, Class, SubClass);
