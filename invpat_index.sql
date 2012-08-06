CREATE INDEX idx_assignee on invpat(assignee);
CREATE INDEX idx_firstlastname on invpat ( firstname, lastname );
CREATE INDEX idx_firstname on invpat(firstname);
CREATE UNIQUE INDEX idx_invnum on invpat (Invnum);
CREATE INDEX idx_lastname on invpat(lastname);
CREATE INDEX idx_patent on invpat(patent);
CREATE UNIQUE INDEX index_invnum_on_invpat ON invpat(invnum);
