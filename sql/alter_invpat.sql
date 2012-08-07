-- Use these statements to start the migration from the existing
-- `invpat_final.sqlite3` database (found on DVN) to a structure
-- which ultimately allows very easy insertion of new data
-- as patents are released weekly.
alter table invpat add column Unique_Record_ID;
alter table invpat add column Middlename;
alter table invpat add column Coauthor;
alter table invpat add column ApplyYear;
alter table invpat add column AppYear;
alter table invpat add column AppDate;
alter table invpat add column Invnum_N;
alter table invpat add column Latitude;
alter table invpat add column Longitude;
UPDATE invpat SET Unique_Record_ID = Invnum;
UPDATE invpat SET Middlename = Firstname;
UPDATE invpat SET Coauthor = "";
UPDATE invpat SET ApplyYear = AppYearStr;
UPDATE invpat SET AppYear = AppYearStr;
UPDATE invpat SET AppDate = AppDateStr;
UPDATE invpat SET Invnum_N = Invnum;
UPDATE invpat SET Latitude = Lat;
UPDATE invpat SET Longitude = Lon;
