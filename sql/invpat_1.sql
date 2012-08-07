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

-- Add new indexes conforming to preprocessing schema...


