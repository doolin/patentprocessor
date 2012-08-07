CREATE INDEX asg on invpat (Assignee);
CREATE INDEX asg2 on invpat (AsgNum);
CREATE INDEX gyr on invpat (Gyear);
CREATE INDEX iNidx  ON invpat (Invnum_N);
CREATE INDEX locc on invpat (City);
CREATE INDEX loccs on invpat (City, State);
CREATE INDEX locs on invpat (State);
CREATE INDEX pdx ON invpat (Patent);
CREATE INDEX pidx ON invpat (Patent, InvSeq);
