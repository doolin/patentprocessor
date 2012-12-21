""" 
 2012/06/28:
  * DB and TBL/TABLE variables represent DB and TBL options
  * Added underscore functions
  * Add a debug option?

"""

def MySQL_cfg(cfg=None, title=None):
    import os, getpass
    if title!=None:
        print title
    if cfg==None:
        cfg = {}
    if "host" not in cfg:
        cfg["host"] = raw_input("host: ")
    if "user" not in cfg:
        cfg["user"] = raw_input("user: ")
    if "passwd" not in cfg:
        cfg["passwd"] = getpass.getpass("passwd: ")
    if "db" not in cfg:
        cfg["db"] = raw_input("db: ")
    return cfg



class SQLite:
    """
    The following is a wrapper for sqlite3, a commonly used library for creating
    transportable relational databases
     * Syntax can be found @ http://www.sqlite.org
     * Python documentation can be found @ http://docs.python.org/library/sqlite3.html
     * Can pass db, tbl to most parameters with **kwargs
    """
    def __init__(self, path=":memory:", db=None, tbl="main", output=False):
        """
        Creates and opens a database connection for
        "path" and default the table to "tbl"

        Args:
          path: the location of the database
          db: the location of the database **legacy
          tbl: the name of the primary table
        Returns: Nothing
          Sets self variables such as tbl, path, c (cursor), conn (connect)
        """
        import sqlite3
        self.path = path
        if db:
            self.path = db
        self.tbl = tbl
        self.conn = sqlite3.connect(self.path)
        self.c = self.conn.cursor()
        self.output = output

    def __del__(self):
        """
        Destructor running similar to a Garbage Collector
        """
        self.close()

    def open(self):
        """
        Opens the connection.
        """
        import sqlite3
        self.conn = sqlite3.connect(self.db)
        self.c = self.conn.cursor()

    #-------------------------------------HIDDEN METHODS

    def _getSelf(self, field=None, **kwargs):
        """
        GETS basic SELF defined variables (ie. self.tbl)

        Args:
          fields: specified files to return
          **kwargs: keyword arguments related self. variables
        Return:
          returns variables in sequence provided
          if list is length one, return string
        *NOTE: self.__dict__ returns a list of 
               avaiable SELF defined variables
        """
        list = []
        alias = {"table": "tbl", "tbl": "table"}
        if not field:
            field = kwargs.keys()

        for key in sorted(field):
            if key in alias and alias[key] in kwargs:
                value = kwargs[alias[key]]
            elif key not in kwargs:
                value = None
            else:
                value = kwargs[key]
            if not value:
                if key in self.__dict__:
                    value = self.__dict__[key]
                elif key in alias and alias[key] in self.__dict__:
                    value = self.__dict__[alias[key]]
            list.append(value)
        if len(list)==1:
            return list[0]
        else:
            return list

    def _dbAdd(self, **kwargs):
        """
        IF db exists, db.tbl ELSE tbl
        """
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        str = ""
        if db:
            str += (db+".")
        str += tbl
        return str

    def _decode(self, list):
        """
        TODO: Is this necessary?  What does this really do?
        """
        try:
            return [x.decode("iso-8859-1") for x in list]
        except:
            return list

    # TODO: Need to test 4 cases, at least. Also, the if
    # statements are not mutually exclusive, so be careful.
    def _keyList(self, key, lower=False, **kwargs):
        """
        Convert key to List of keys if string or if "keys"
        """
        #print "kwargs from _keyList: ", kwargs
        if "keys" in kwargs: #2012/07/01 to depreciate "keys"
            key = [kwargs["keys"]]
            #print "from 'if \"keys\"'..."
        if type(key).__name__ in ('unicode', 'str'):
            key = [key]
            #print "from 'type(key).__name__'..."
        if lower:
            key = set([k.lower() for k in key])
            #print "from 'if lower:'..."
        #print "key from inside _keyList..."
        return key

    def _sqlmasterScan(self, var, type, lookup=None, db=None, seq=None):
        """
        Returns a list of items that exist within the database.
        *since SQLite is not case sensitive, lowercases everything

        Arg
          var: field to return
          type: type in database such as table, index
          db: consider a specific database?
          lookup: are we considering a specific item?
          seq: returns a range of indexes for numbering purposes
        Returns:
          a list of names that exist within the database.
          unless lookup specified: true or false
        """
        self.c.execute(""" 
            SELECT {var} FROM {table} 
             WHERE type='{type}' AND {var} IS NOT NULL ORDER BY {var}
            """.format(var=var, type=type,
              table=self._dbAdd(db=db, tbl="sqlite_master"))) #"""
        list = [x[0].lower() for x in self.c]
        if seq:
            import re
            nums = []
            for x in list:
                if x.find(seq)==0:
                    d = re.findall('[0-9]+$', x)
                    if not d:
                        nums.append(1)
                    else:
                        nums.append(int(d[-1]))
            if not nums:
                return [0, 0]
            else:
                return [min(nums), max(nums)]
        elif not lookup:
            return list
        else:
            return lookup.lower() in list

    def _baseIndex(self, idx=None, **kwargs):
        """
        Boils down a Index to its most basic form. ie. table (keys)

        Args:
          idx: a specific index SQL to process or name of index
            if None specified, process all indexes
        Return:
          if processing all indexes, list of barebore indexes
        """
        import re
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)

        if idx==None:
            self.c.execute("SELECT sql FROM {tbl} WHERE type='index' AND sql IS NOT NULL".\
                format(tbl=self._dbAdd(db=db, tbl="sqlite_master")))
            sqls = self.c.fetchall()
        else:
            self.c.execute("SELECT sql FROM {tbl} WHERE type='index' AND name='{idx}' AND sql IS NOT NULL".\
                format(tbl=self._dbAdd(db=db, tbl="sqlite_master"), idx=idx))
            sqls = self.c.fetchall()
            # if index name doesn't exist assume SQL statement
            if not len(sqls):
                sqls = [[idx,]]

        #simplify the list
        idxLst = []
        for sql in sqls:
            sql = re.sub("index .*? on", "", sql[0].lower())
            sql = re.sub(", ", ",", sql)
            sql = re.sub("  +", " ", sql)
            sql = sql.replace("create ", "")
            schema = re.findall("[(].*?[)]", sql)[0][1:-1]
            #reorder the keys
            sql = sql.replace(schema, ",".join(sorted(schema.split(","))))
            idxLst.append(sql)

        if idx:
            return idxLst[0]
        else:
            return idxLst

    #-------------------------------------BACKGROUND FX

    def close(self):
        """
        Initiates a final commit (assumption, we want to commit data)
        Closes the appropriate cursors and connections 
        *chosen not to TEST this method
        """
        if self.c:
            self.commit()
            self.c.close()
            self.conn.close()
            self.c = None

    def optimize(self):
        """ 
        Optimize based on guidance found on the following:
          http://web.utk.edu/~jplyon/sqlite/SQLite_optimization_FAQ.html
        *chosen not to TEST this method
        """
        self.c.executescript(""" 
            PRAGMA cache_size=2000000;
            PRAGMA synchronous=OFF;
            PRAGMA temp_store=2;
            """) #"""

    def getTbl(self, table=None):
        if table==None:
            return self.tbl
        else:
            return table

    def chgTbl(self, tbl):
        """
        Allows a user to change their default table
        *chosen not to TEST this method
        """
        self.tbl = tbl

    def commit(self):
        """
        Alias to self.conn.commit()
        *chosen not to TEST this method
        """
        self.conn.commit()

    def vacuum(self):
        """
        Databases expand with records.  This command compresses them to their
        smallest states.
        *chosen not to TEST this method
        """
        self.c.execute("vacuum")
        self.commit()

    #-------------------------------------TABLE MANIPULATION

    # The original definition of add, used by `clean.py`.
    # TODO: Fix clean.py and delete this function
    def add(self, key, typ="", table=None):
        import types
        table = self.getTbl(table)
        if type(key) != types.ListType:
            key = [key]
        for k in key:
            try:
                self.c.execute("ALTER TABLE %s ADD COLUMN %s %s" % (table, k, typ))
            except:
                pass

    # The add function was changed on June 30, and this new definition won't
    # work with the call in clean.py
    # TODO: Reconcile the calling function with the new definition.
    def add_new(self, key=None, **kwargs):
        """
        Allows one the ability to add columns to SQLite table
        **update 2012/06/30: 
          removed the typ variable
          now key should be a dictionary type
          will deprecaite key=None to just key

        Args:
          key: {key: value} <==> synonym is keys
            input can be list, tuple, str, unicode, dict
            converts to dict {key: type}
            default type is blank
        """
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        if "keys" in kwargs:
            key = kwargs["keys"]
        if type(key).__name__ in ('unicode', 'str'):
            key = {key: ""}
        elif type(key).__name__ in ('list', 'tuple'):
            key = dict([[k, ""] for k in key])

        for k,v in key.items():
            if "typ" in kwargs:
                v = kwargs["typ"] #2012/06/30 to deprecaite typ
            if not self.columns(lower=True, lookup=k, **kwargs):
                self.c.execute("""
                    ALTER TABLE {table} ADD COLUMN {name} {type}
                    """.format(table=self._dbAdd(
                        db=db, tbl=tbl), name=k, type=v)) #"""

    def drop(self, key=None, **kwargs):
        """
        Allows one the ability to drop columns in SQLite table
        This function doesn't exist in SQLite.  Better to do this earlier as it requires SQL.
        **update 2012/06/30: 
            modified default "keys" to "key"
            will deprecaite they "keys" option over time and require key

        Args:
          key: list of column keys to remove <==> synonym is keys
            input can be list, tuple, str, unicode
            default type is blank
        Note: dropping an attached table doesn't matke sense so
          db has been removed
        """
        import csv, re, StringIO
        tbl = self._getSelf(field=["tbl"], **kwargs)
        indexes = []
        baseIdx = []
        key = self._keyList(key, lower=True, **kwargs)
        col = set(self.columns(lower=True, **kwargs)) - key

        #manipulate the table
        self.c.execute("SELECT sql,type FROM {tbl} WHERE tbl_name='{where}' AND sql is not NULL".\
            format(tbl="sqlite_master", where=tbl))
        sqls = self.c.fetchall()

        #sometimes the sql can get complicated
        for sql, typ in sqls:
            sql = re.sub("[\n\t]", "", sql)
            schema = re.findall("[(].*[)]", sql, re.S)[0][1:-1]
            sql = sql.replace(schema, "{schema}")

            schema = [s.strip() for s in schema.split(",")]
            schCsv = [csv.reader(StringIO.StringIO(s)).next()
                         for s in schema]

            #remove part of the SQL structure
            for k in key:
                for s in schCsv:
                    if k.lower() == s[0].lower():
                        schema.pop(schCsv.index(s))
                        schCsv.remove(s)

            sql = sql.format(schema=", ".join(schema))
            if len(schema):
                if typ=="table":
                    tblSql = sql
                else:
                    indexes.append(sql)

        self.c.executescript(""" 
            DROP TABLE IF EXISTS {tbl}_backup;
            ALTER TABLE {tbl} RENAME TO {tbl}_backup;
            {tblSql};
            INSERT INTO {tbl} ({schema})
                SELECT {schema} FROM {tbl}_backup;
            DROP TABLE {tbl}_backup;
            """.format(tbl=tbl, schema=",".join(col), tblSql=tblSql)) #"""

        for sql in indexes:
            # figure out a base to remove redundancies
            base = self._baseIndex(idx=sql)
            if base not in baseIdx:
                baseIdx.append(base)
                self.c.execute(sql)

    def delete(self, key=None, **kwargs):
        """
        Equivalent to DROP table 
        Args:
          key: string or list of tables
        """
        key = self._keyList(key, **kwargs)
        for k in key:
            self.c.execute("DROP TABLE IF EXISTS {tbl}".format(tbl=k))

    def index(self, key=None, index=None, unique=False, combo=False, **kwargs):
        """
        Creates an index on the table.

        Args:
          key: Modified default keys to key.  These are the columns to index.
          index: Name of index to modify
          unique: Is the index unique?
          combo: Do we want to index all combinations of keys?
             ie. if combo True: [a,b] indexes [a], [b] and [a,b]
        Return:
          if successful indexing occurs, return name of index
        """

        import re
        import itertools
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        key = self._keyList(key, lower=True, **kwargs)

        if combo:
            for x in xrange(len(key)):
                for k in itertools.combinations(key, x+1):
                    self.index(key=k, index=index, unique=unique, **kwargs)

        if not index:
            seq = self.indexes(seq="idx_idx", db=db)
            index = "idx_idx{num}".format(num=seq[-1] and seq[-1]+1 or "")

        idxBase = self._baseIndex(**kwargs)
        #building an index
        idxNew = ["CREATE"]
        if unique:
            idxNew.append("UNIQUE")
        idxNew.extend(["INDEX", self._dbAdd(db=db, tbl=index), 
            "ON", tbl, "({key})".format(key=",".join(key))])
        idxNew = " ".join(idxNew)

        if not set(key) <= set(self.columns(lower=True, **kwargs)):
            return None #are keys a subset of columns?
        elif self._baseIndex(idx=idxNew, **kwargs) not in idxBase:
            self.c.execute(idxNew)
            return self._dbAdd(db=db, tbl=index)
        else:
            #TODO should we return the name of the index otherwise?
            return None

    #-------------------------------------STATS LIKE

    def tables(self, lookup=None, db=None, seq=None):
        #returns a list of tables or existence of a table
        return self._sqlmasterScan(var="tbl_name", 
            type="table", lookup=lookup, db=db, seq=seq)

    def indexes(self, lookup=None, db=None, seq=None):
        #returns a list of indexes or existence of a index
        return self._sqlmasterScan(var="name", 
            type="index", lookup=lookup, db=db, seq=seq)

    #-------------------------------------REPORTS

    def columns(self, lower=False, lookup=None, **kwargs):
        """ 
        Basic report that showcases columns

        Args:
          lower: lowercase the column names
          lookup: find a column within the columns
        Return:
          returns a list of columns or existence of column
        """
        db, output, tbl = self._getSelf(
            field=["db", "tbl", "output"], **kwargs)
        self.c.execute("PRAGMA %s" % (
           self._dbAdd(db=db, tbl="TABLE_INFO("+tbl+")")))
        list = []
        if lower and lookup:
            lookup = lookup.lower()
        for row in self.c:
            if output and not lookup: print row
            if lower:
                list.append(row[1].lower())
            else:
                list.append(row[1])
        if lookup:
            return lookup in list
        else:
            return list

    def count(self, **kwargs):
        """
        Basic report with time and date

        Args:
          default is time stamp and count (if output on)
        Return:
          returns the number of records for the table
        """
        import datetime
        db, output, tbl = self._getSelf(
            field=["db", "tbl", "output"], **kwargs)
        if self.tables(lookup=tbl, db=db):
            cnt = self.c.execute("SELECT count(*) FROM {table}".\
                format(table=self._dbAdd(db=db, tbl=tbl))).fetchone()[0]
        else:
            cnt = 0
        if output:
            print datetime.datetime.now(), cnt
        return cnt

    #-------------------------------------ANALYSIS

    def fetch(self, field="*", random=False, 
              limit=None, iter=False, **kwargs):
        """ 
        Replicates common function where you return an array of values
        associated with a SQLite table

        Args:
          field: specific fields?
          limit: return a specific length of items?
          random: return data in a random sequence?
        Return: This is based on the iterator. 
        """
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        if type(field).__name__ in ("list", "tuple"):
            field = ",".join(field)

        query = ["SELECT", field, "FROM", self._dbAdd(db=db, tbl=tbl)]
        if random:
            query.append("ORDER BY random()")
        if limit:
            query.extend(["LIMIT", str(limit)])
        query = " ".join(query)

        if not self.tables(lookup=tbl, db=db):
            return []
        elif iter:
            return self.c.execute(query)
        else:
            return self.c.execute(query).fetchall()

    #-------------------------------------DATABASE MGMT

    def attach(self, db, name="db"):
        """ 
        Attaches the "db" database as "name"

        Args:
          db: path or SQLite of database to attach
            *if SQLite, defaults to its path
          name: the alias of the database

        *chosen not to TEST this method
        """
        if db.__class__.__name__ == 'SQLite':
            db = db.path
        self.detach(name=name)
        self.c.execute("ATTACH DATABASE '{db}' AS {name}".format(db=db, name=name))

    def detach(self, name="db"):
        """ 
        Detaches the database "name"
        *chosen not to TEST this method
        """
        try:
            self.c.execute("DETACH DATABASE {name}".format(name=name))
        except:
            pass

    def replicate(self, tableTo=None, **kwargs):
        """ 
        Replicates the basic structure of a table to another table

        Args:
          tableTo: replicate db.tbl to tableTo.  Basic assumption is default to self.tbl.
        """
        import re
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        if not tableTo:
            tableTo = self.tbl

        self.c.execute(""" 
            ALTER TABLE {table} RENAME TO {tblTo}
            """.format(tblTo=tableTo,
                       table=self._dbAdd(tbl=tbl, db=db))) #"""
        self.c.execute(""" 
            SELECT sql FROM {table} WHERE tbl_name='{where}' AND type='table' AND sql IS NOT NULL
            """.format(table=self._dbAdd(db=db, tbl="sqlite_master"), 
                       where=tableTo)) #"""
        sqlTbl = self.c.fetchone()[0]
        self.c.execute(""" 
            SELECT sql, name FROM {table} WHERE tbl_name='{where}' AND type!='table' AND sql IS NOT NULL
            """.format(table=self._dbAdd(db=db, tbl="sqlite_master"), 
                       where=tableTo)) #"""
        sqlOth = self.c.fetchall()
        self.c.execute(""" 
            ALTER TABLE {table} RENAME TO {tblTo}
            """.format(tblTo=tbl,
                       table=self._dbAdd(tbl=tableTo, db=db))) #"""

        self.c.execute(sqlTbl)
        for sql, name in sqlOth:
            schema = re.findall("[(].*?[)]", sql, re.S)[0][1:-1]
            sql = sql.replace(schema, "{schema}")
            # TODO: replace is probably not enough.  what if index is called "E"?
            #       could cause some issues.. since CREATE INDEX ...
            sql = sql.replace(name, tableTo+"_"+name)
            sql = sql.format(schema=schema)
            self.c.execute(sql)

    #-------------------------------------DATA INPUT

    def csvInput(self, path, iter=False, **kwargs):
        """ 
        Takes a CSV like file and processes into a iterator or list

        Args:
          file: self evident
          iterator: return a list or return an iterator?
          **kwargs are mostly for the CSV parser
            http://docs.python.org/library/csv.html
            can do things like delimiter
        Return: This is based on the iterator. 
        """
        if "db" in kwargs:
            del kwargs["db"]
        if "tbl" in kwargs:
            del kwargs["tbl"]

        import csv
        file = open(path, "rb")
        if iter:
            return csv.reader(file, **kwargs)
        else:
            return [x for x in csv.reader(file, **kwargs)]

    def insert(self, data=None, field=None, ignore=True, header=False, errlog=None, **kwargs):
        """ 
        Replicates an INSERT INTO command.  
        Generates a table if specified table does not exist.

        Args:
           data: the data, can be list of lists,
             list of dictionaries, iter (such as reader or Cursor) 
             dictionaries specify the variable to insert into, 
             otherwise field is considered
             if data=None:
               assumes we are inserting data into our current table 
               specified through the tbl, db arguments
           field: the fields to consider for inserting
             if this is blank, insert following the table schema
           ignore: for unique tables should we IGNORE or REPLACE?
           header: is the first column of data essentially the fields?
             this is common with csv files and the like
           errlog: Error log 

        Error checking*  UNICODE is a known issue
        """
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)
        def buildInsert(field, ignore, tbl):
            sql = ["INSERT", "OR"]
            if ignore:
                sql.append("IGNORE")
            else:
                sql.append("REPLACE")
            sql.extend(["INTO", tbl])
            if field:
                sql.append("({schema})".format(schema=",".join(field)))
            return sql

        if not data:
            # assuming we are inserting data from a seperate table
            # assuming field names are the same
            sql = buildInsert(field, ignore, self.tbl)
            sql.append("SELECT")
            if field:
                sql.append(",".join(field))
            else:
                sql.append("*")
            sql.extend(["FROM", self._dbAdd(db=db, tbl=tbl)])
            sql = " ".join(sql)
            self.c.execute(sql)
        else:
            if errlog:
                err = open(errlog, "wb")

            if type(data).__name__ in ('dict'):
                data = [data]
            elif type(data).__name__ in ('list', 'tuple'):
                if type(data[0]).__name__ not in ('list', 'tuple', 'dict'):
                    data = [data]
            data = iter(data)

            if header:
                field = data.next()

            for i,d in enumerate(data):
                if type(d).__name__ in ('dict'):
                    d = d.items()
                    f = [x[0] for x in d] #fields
                    d = [x[1] for x in d] #data
                else:
                    f = field
                sql = buildInsert(f, ignore, self._dbAdd(db=db, tbl=tbl))
                sql.extend(["VALUES", "("+(",".join(["?"]*len(d)))+")"])

                # if the table doesn't exist build it now
                if not self.tables(lookup=tbl) and i==0:
                    if field:
                        schema = ",".join(field)
                    else:
                        schema = ",".join(
                            ["v"+str(i) for i in xrange(1, len(d)+1)])
                    self.c.execute("""
                        CREATE TABLE {tbl} ({schema})
                        """.format(tbl=tbl, schema=schema)) #"""

                sql = " ".join(sql)
                try:
                    self.c.execute(sql, d)
                #build in error handling for unicode?
                except:
                    if errlog:
                        err.write(sql)
                        err.write("\n")
                        err.write(", ".join(d))
                        err.write("\n")
                        err.write("--------------")
                        err.write("\n")


    def addSQL(self, data, header=False, field=None, ignore=True, errlog=None, **kwargs):
        """
        This serves as a convenience function to INSERT

        Args:
          data: can be filename, table or pure data
            uses INSERT function to manage the rest
         *paramters match the INSERT very carefully
        """
        import types, os
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)

        if type(data).__name__ in ('str', 'unicode'):
            #if this is a real file
            if os.path.exists(data):
                data = self.csvInput(data, iter=True, **kwargs)
                self.insert(data=data, field=field, header=header, ignore=ignore, errlog=errlog, db=db, tbl=tbl)
            #this is a table, copy contents from one table > another
            else:
                self.insert(tbl=data, db=db, field=field, header=header, ignore=ignore, errlog=errlog)
        else:
            #this is data, just execute the insert command
            self.insert(data=data, field=field, header=header, ignore=ignore, errlog=errlog)


    def merge(self, key, on, tableFrom, keyType=None, **kwargs):
        """
        *Will come back to this function

        Matches the on variables from two tables and updates the key values

        Example of usage: (its on the table perspective, so that's first)
        On and Keys take an iterable with values of string or list:

        ie.
        key = ["ed", ["eric", "amy"]]
        on = ["ron", ["ron1", "amy"]]
        keyType = ['VARCHAR', 'VARCHAR'] #if nothing will just be blanks

        All together:

        .add('ed', 'VARCHAR')
        .add('eric', 'VARCHAR')

        c.executemany("UPDATE table SET ed=?, eric=? WHERE ron=? AND ron1=?",
            c.execute("SELECT b.ed, b.amy, b.ron, b.amy
                         FROM table AS a INNER JOIN tableFrom AS b
                           ON a.ron=b.ron AND a.ron1=b.amy").fetchall())
        """

        def huggleMe(lst, idx=0, head="", tail="", inner=", "):
            return head+("%s%s%s" % (tail, inner, head)).join([x[idx] for x in lst])+tail

        import types, datetime
        db, tbl = self._getSelf(field=["db", "tbl"], **kwargs)

        key = [type(x)==types.StringType and [x,x] or x for x in key]
        on =  [type(x)==types.StringType and [x,x] or x for x in on]

        for i,x in enumerate(key):
            self.add(x[0], keyType!=None and keyType[i] or "", tbl=tbl)

        idxT = self.index(keys=[x[0] for x in on], tbl=tbl)
        idxF = self.index(keys=[x[1] for x in on], tbl=tableFrom, db=db)

        self.c.executescript(""" 
            DROP TABLE IF EXISTS TblA;
            DROP TABLE IF EXISTS TblB;
            CREATE TEMPORARY TABLE TblA AS SELECT %s FROM %s GROUP BY %s;
            CREATE TEMPORARY TABLE TblB AS SELECT %s, %s FROM %s GROUP BY %s;
            """ % (huggleMe(on), table, huggleMe(on),
                   huggleMe(key, idx=1), huggleMe(on, idx=1), self._dbAdd(db=db, tbl=tableFrom), huggleMe(on, idx=1))) #"""
        self.index(keys=[x[0] for x in on], tbl="TblA", index='idx_temp_TblA')
        self.index(keys=[x[1] for x in on], tbl="TblB", index='idx_temp_TblB')

        sqlS = "UPDATE %s SET %s WHERE %s" % (tbl, huggleMe(key, tail="=?"), huggleMe(on, tail="=?", inner=" AND "))
        sqlV = "SELECT %s, %s FROM TblA AS a INNER JOIN TblB AS b ON %s" % (
            huggleMe(key, idx=1, head="b."), huggleMe(on, idx=1, head="b."),
            " AND ".join(["a."+"=b.".join(x) for x in on]))
        vals = self.c.execute(sqlV).fetchall()
        if len(vals)>0:
            self.c.executemany(sqlS, vals)

        #remove indices that we just temporarily created
        for x in [idxT, idxF]:
            if x!=None:
                self.c.execute("DROP INDEX %s" % x)

    # STOPPED AT THIS POINT

    # DEPRECIATE THIS FUNCTION?
    def quickSQL(self, data, override=False, header=False, allVars=False, typescan=50, typeList=[], **kwargs):
        """
            allVars => Make all variables VARCHARS (IGNORE BUILDING TYPE)
        """
        import re, types
        tbl = self._getSelf(field=["tbl"], **kwargs)

        if override:
            self.c.execute("DROP TABLE IF EXISTS %s" % table)
        elif self.tables(db=None, lookup=table):
            return

        if header:
            headLst = []
            for x in data[0]:
                headLst.append(re.sub("[()!@$%^&*'-]+", "", x).replace(" ", "_").replace("?", ""))
                if headLst[-1] in headLst[:-1]:
                    headLst[-1]+=str(headLst[:-1].count(headLst[-1])+1)

        tList = []
        for i,x in enumerate(data[1]):
            if str(typeList).upper().find("%s " % data[0][i].upper())<0:
                cType = {types.StringType:"VARCHAR", types.UnicodeType:"VARCHAR", types.IntType:"INTEGER", types.FloatType: "REAL", types.NoneType: "VARCHAR"}[type(x)]
                if type(typescan)==types.IntType and cType=="VARCHAR":
                    least = 2
                    ints = 1

                    for j in range(1, min(typescan+1, len(data))):
                        if type(data[j][i])==types.StringType or type(data[j][i])==types.UnicodeType:
                            if re.sub(r"[-,.]", "", data[j][i]).isdigit():
                                if len(re.findall(r"[.]", data[j][i]))==0:   pass
                                elif len(re.findall(r"[.]", data[j][i]))==1: ints = 0
                                else: least = 0; break
                            else: least = 0; break

                    cType = {0:"VARCHAR", 1:"INTEGER", 2:"REAL"}[max(least-ints, 0)]

                if header:
                    if allVars:
                        tList.append("%s" % (headLst[i],))
                    else:
                        tList.append("%s %s" % (headLst[i], cType))
                else:
                    if allVars:
                        tList.append("v%d" % (i,))
                    else:
                        tList.append("v%d %s" % (i, cType))

            else:
                tList.extend([y for y in typeList if y.upper().find("%s " % data[0][i].upper())==0])

        self.c.execute("CREATE TABLE IF NOT EXISTS %s (%s)" % (table, ", ".join(tList)))
        if header==False:
            self.c.executemany("INSERT INTO %s VALUES (%s)" % (table, ", ".join(["?"]*len(data[0]))), data)
        else:
            self.c.executemany("INSERT INTO %s VALUES (%s)" % (table, ", ".join(["?"]*len(data[0]))), data[1:])
        self.conn.commit()


    #----- OUTPUTS -----#

    def csv_output(self, fname="default.csv", table=None):
        """
            Exports data into a CSV which is defaulted to "default.csv"
        """
        import unicodedata
        def asc(val):
            return [unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') for x in val]

        import csv
        if not table:
            table = self.tbl
        f = open(fname, "wb")
        writer = csv.writer(f, lineterminator="\n")
        writer.writerows([self.columns(table, output=False)])
        writer.writerows([asc(x) for x in self.c.execute("SELECT * FROM %s" % table).fetchall()])
        writer = None
        f.close()

    def mysql_output(self, cfg={'host':'localhost', 'db':'RD'}, textList=[], intList=[], varList=[], tableTo=None, table=None, full=True):
        """
        Output table into MySQL database.
        Auto converts fields TEXT, VARCHAR, and [Blank] to VARCHAR(255)
        Add additional text field names by using the textList
            (useful for the incorrect fields) tableTo is the MySQL table
        Add additional integer field names by using the intList
        Add additional varList.  This allows you to specify whatever you want.
            Format: [["name", "format"]]

        Full = True (input data)
        """
        textList = [x.lower() for x in textList]
        intList = [x.lower() for x in intList]

        if varList!=[]:
            varList = zip(*varList)
            varList[0] = [x.lower() for x in varList[0]]
        cfg = MySQL_cfg(cfg)

        import MySQLdb, re, types, unicodedata, sys, datetime
        if not table:
            table = self.tbl
        if tableTo == None:
            tableTo = table
        def field(name, type):
            name = name.lower()
            type = type.lower()

            if varList!=[] and name in varList[0]:
                return varList[1][varList[0].index(name)]
            if name in textList:
                return "VARCHAR(64)";
            elif name in intList:
                return "INTEGER";
            elif type.find("varchar")>=0 or type=="text" or type=="":
                return "VARCHAR(64)";
            elif type.find("int")>=0:
                return "INTEGER";
            elif type.find("real")>=0:
                return "REAL";
            else:
                return type

        mconn = MySQLdb.connect(host=cfg['host'], user=cfg['user'], passwd=cfg['passwd'], db=cfg['db'])
        mc = mconn.cursor()
        #get column and types for fields
        cols = ["`%s` %s" % (x[1], field(x[1], x[2])) for x in self.c.execute("PRAGMA TABLE_INFO(%s)" % table)]
        sql = "CREATE TABLE %s (%s);" % (tableTo, ", ".join(cols))

        try:
            mc.execute(sql)
        except:
            y=0
        indexes = [x[0] for x in self.c.execute("SELECT sql FROM sqlite_master WHERE type='index' AND tbl_name='%s' AND sql IS NOT NULL"  % table)]

        for idx in indexes:
            if idx!=None:
                idx = idx.lower()
                idx = idx.replace('on %s (' % table.lower(),
                                  'on %s (' % tableTo)
                try:
                    #print idx
                    mc.execute(idx)
                except:
                    y=0
                    print "Error:", idx

        if full:
            self.c.execute("SELECT * FROM %s" % table)
            t0 = datetime.datetime.now()
            i = 0
            while True:
                i = i + 1
                val = self.c.fetchone()
                if not val:
                    break

                insert = [(type(x)==types.UnicodeType or type(x)==types.StringType) and
                          unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') or x for x in val]
                try:
                    mc.execute("INSERT IGNORE INTO %s VALUES (%s)" % (tableTo, ", ".join(["%s"]*len(cols))), insert)
                except:
                    print i,val
                sys.stdout.write("{clear}  - {x} {time}".format(clear="\b"*30, x=i, time=datetime.datetime.now()-t0))
            print ""

##            vals = [x for x in self.c.execute("SELECT * FROM %s" % table)]                
##            for i,val in enumerate(vals):
##                #this is done to normalize the data
##                insert = [(type(x)==types.UnicodeType or type(x)==types.StringType) and
##                          unicodedata.normalize('NFKD', unicode(x)).encode('ascii', 'ignore') or x for x in val]
##                try:
##                    mc.execute("INSERT IGNORE INTO %s VALUES (%s)" % (tableTo, ", ".join(["%s"]*len(cols))), insert)
##                except:
##                    print i+1,val

        mc.close()
        mconn.close()

    """
    EXPERIMENTAL FUNCTIONS
    """
    # IGRAPH / VISUALIZATION RELATED FUNCTIONS, very very preliminary

    def igraph(self, where, table=None,
                 vx="Invnum_N", ed="Patent", order="AppYear",
                 va=", Lastname||', '||Firstname AS Name, City||'-'||State||'-'||Country AS Loc, Assignee, AsgNum",
                 ea=", a.AppYear AS AppYear", eg=', a.AppYear'):
        import math, datetime, senGraph
        if not table:
            table = self.tbl
        tab = senGraph.senTab()
        self.c.executescript("""
            DROP TABLE IF EXISTS G0;
            DROP TABLE IF EXISTS vx0;
            DROP TABLE IF EXISTS ed0;
            CREATE TEMP TABLE G0 AS
                SELECT * FROM %s WHERE %s ORDER BY %s;
            CREATE INDEX G_id ON G0 (%s);
            CREATE INDEX G_ed ON G0 (%s, %s);
            CREATE TEMPORARY TABLE vx0 AS
                SELECT %s, count(*) AS Patents %s FROM G0
                 GROUP BY %s;
            CREATE INDEX vx_id ON vx0 (%s);
            CREATE TEMPORARY TABLE ed0 AS
                SELECT  a.%s, b.%s, a.%s AS hId, b.%s AS tId, count(*) AS Weight %s
                  FROM  G0 AS a INNER JOIN G0 AS b
                    ON  a.%s=b.%s AND a.%s<b.%s
              GROUP BY  a.%s, b.%s %s;
            """ % (table, where, order, ed, vx, ed, vx, va, vx, vx,
                   vx, vx, vx, vx, ea, ed, ed, vx, vx, vx, vx, eg))

        tab.vList = self.c.execute("SELECT * FROM vx0").fetchall()
        tab.vlst = self.columns(table="vx0", output=False)[1:]
        tab.eList = self.c.execute("SELECT * FROM ed0").fetchall()
        tab.elst = self.columns(table="ed0", output=False)[2:]
        s = senGraph.senGraph(tab, "vertex")
        return s
