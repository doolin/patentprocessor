# Preprocessing patent data


## Raw data

* USPTO via Google


## NBER  


1. Went to 
[https://sites.google.com/site/patentdataproject/Home/downloads]
(https://sites.google.com/site/patentdataproject/Home/downloads), 
downloaded assignee.zip (file of patent assignees including name and unique assignee number PDPASS), created assignee.csv

2. FTP’ed assignee.csv to XML folder on patbox
3. Created NBER_asg.sqlite3
4. Created NBER database table

~~~~

>> from SQLite import *
>> from senAdd import *
>> s = SQLite(‘NBER_asg’) #open this database, creates table ‘main’
>> s.addSQL(data = ‘assignee.csv’, header = True)
#add in data from assignee.csv
# with columns using headers of csv file
>> s.c.execute(“select * from main limit 10”).fetchall()
# table name will always be main
# cursor will always be c
                                >> s.columns()
>> s.conn.create_function(“ascit”, 1, ascit)
>>  s.c.execute(“alter table main add column assignee varchar(30);”)
>> s.c.execute(“update main set assignee = ascit(standard_name)”)
>> s.close()
 
~~~~

* http://stackoverflow.com/questions/228912/sqlite-parameter-substitution-problem
 
By the way, it looks like they have since updated the available 
downloads such that now they are in ASCII format (the file is now
called assignee.asc.zip), so you may not need to do the type
conversion if you are looking to recreate the process.




* SAS States, Territories, Associated Areas of the United States is a
  National file that contains Longitudinal and Latitude information for
cities across the states.  http://geonames.usgs.gov/domestic/download_data.htm 

* GNS  National Geospatial-Intelligence Agency country files


