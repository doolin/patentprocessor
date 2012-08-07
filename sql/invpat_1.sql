-- What we want is to be able to parse the weekly patent data
-- and insert it very easily into the existing database. Making
-- this really easy requires using the same schema in the database
-- that is used by the preprocessor.

CREATE TABLE invpat_1(
        Firstname TEXT,
        Middlename TEXT,
        Lastname TEXT,
        Street TEXT,
        City TEXT,
        State TEXT,
        Country TEXT,
        Zipcode TEXT,
        Latitude REAL,
        Longitude REAL,
        InvSeq INT,
        Patent TEXT,
        AppYear TEXT,
        ApplyYear TEXT,
        GYear INT,
        AppDate TEXT,
        Assignee TEXT,
        AsgNum INT,
        Class TEXT,
        Coauthor TEXT,
        Invnum TEXT,
        Invnum_N TEXT,
        Unique_Record_ID TEXT);

-- Here is where we do the copying to load up the invpat_1 table.
-- Once this is done, we drop the invpat table and recreate it.
INSERT INTO invpat_1(
        Firstname,
        Middlename,
        Lastname,
        Street,
        City,
        State,
        Country,
        Zipcode,
        Latitude,
        Longitude,
        InvSeq,
        Patent,
        AppYear,
        ApplyYear,
        GYear,
        AppDate,
        Assignee,
        AsgNum,
        Class,
        Coauthor,
        Invnum,
        Invnum_N,
        Unique_Record_ID)
SELECT 
        Firstname,
        Middlename,
        Lastname,
        Street,
        City,
        State,
        Country,
        Zipcode,
        Latitude,
        Longitude,
        InvSeq,
        Patent,
        AppYear,
        ApplyYear,
        GYear,
        AppDate,
        Assignee,
        AsgNum,
        Class,
        Coauthor,
        Invnum,
        Invnum_N,
        Unique_Record_ID
FROM invpat;

-- Now we drop the original table...
drop table invpat;

-- ...because we want to recreate it...
CREATE TABLE invpat(
	Firstname TEXT,
        Middlename TEXT,
        Lastname TEXT,
        Street TEXT,
        City TEXT,
        State TEXT,
        Country TEXT,
        Zipcode TEXT,
        Latitude REAL,
        Longitude REAL,
        InvSeq INT,
        Patent TEXT,
        AppYear TEXT,
        ApplyYear TEXT,
        GYear INT,
        AppDate TEXT,
        Assignee TEXT,
        AsgNum INT,
        Class TEXT,
        Coauthor TEXT,
        Invnum TEXT,
        Invnum_N TEXT,
        Unique_Record_ID TEXT);

-- Now, let's repopulate the original table with data conforming
-- to the same schema as the patent preprocessor emits.
INSERT INTO invpat(
        Firstname,
        Middlename,
        Lastname,
        Street,
        City,
        State,
        Country,
        Zipcode,
        Latitude,
        Longitude,
        InvSeq,
        Patent,
        AppYear,
        ApplyYear,
        GYear,
        AppDate,
        Assignee,
        AsgNum,
        Class,
        Coauthor,
        Invnum,
        Invnum_N,
        Unique_Record_ID)
SELECT 
        Firstname,
        Middlename,
        Lastname,
        Street,
        City,
        State,
        Country,
        Zipcode,
        Latitude,
        Longitude,
        InvSeq,
        Patent,
        AppYear,
        ApplyYear,
        GYear,
        AppDate,
        Assignee,
        AsgNum,
        Class,
        Coauthor,
        Invnum,
        Invnum_N,
        Unique_Record_ID
FROM invpat_1;

-- Now we drop all the current indexes... 
DROP INDEX IF EXISTS idx_assignee;
DROP INDEX IF EXISTS idx_firstlastname;
DROP INDEX IF EXISTS idx_firstname;
DROP INDEX IF EXISTS idx_invnum;
DROP INDEX IF EXISTS idx_lastname;
DROP INDEX IF EXISTS idx_lower;
DROP INDEX IF EXISTS idx_patent;
DROP INDEX IF EXISTS idx_upper;
DROP INDEX IF EXISTS index_invnum_on_invpat;


-- Add new indexes conforming to preprocessing schema...
-- Make sure this matches the index file in the sql
-- directory. At some point, this should be controlled
-- by a python or ruby script which reads the same file
-- that the preprocessor reads.
CREATE INDEX asg on invpat (Assignee);
CREATE INDEX asg2 on invpat (AsgNum);
CREATE INDEX gyr on invpat (Gyear);
CREATE INDEX iNidx  ON invpat (Invnum_N);
CREATE INDEX locc on invpat (City);
CREATE INDEX loccs on invpat (City, State);
CREATE INDEX locs on invpat (State);
CREATE INDEX pdx ON invpat (Patent);
CREATE INDEX pidx ON invpat (Patent, InvSeq);

-- And close with a cleanup...
vacuum;
