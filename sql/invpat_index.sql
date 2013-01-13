CREATE INDEX idx_invpat_assignee on invpat (Assignee);
CREATE INDEX idx_invpat_asgnum on invpat (Asgnum);           
CREATE INDEX idx_invpat_gyear on invpat (Gyear);
CREATE INDEX idx_invpat_invnum_n on invpat (Invnum_N);
CREATE INDEX idx_invpat_city on invpat (City);
CREATE INDEX idx_invpat_city_state on invpat (City, State);
CREATE INDEX idx_invpat_state on invpat (State);
CREATE INDEX idx_invpat_patent on invpat (Patent);
CREATE INDEX idx_invpat_patent_invseq on invpat (Patent, Invseq);
