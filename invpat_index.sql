CREATE INDEX idx_assignee on invpat(Assignee);
CREATE INDEX idx_firstlastname on invpat(Firstname, Lastname );
CREATE INDEX idx_firstname on invpat(Firstname);
CREATE UNIQUE INDEX idx_invnum on invpat(Invnum);
CREATE INDEX idx_lastname on invpat(Lastname);
CREATE INDEX idx_patent on invpat(Patent);
