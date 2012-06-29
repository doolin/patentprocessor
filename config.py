basePath = "/home/ronlai/patent"

loc = {
    "db": "{path}/output/loctbl.sqlite3".format(path=basePath),
    "gns": "{path}/input/geonames.txt".format(path=basePath),
    "usloc": "{path}/input/natfile.txt".format(path=basePath),
    "typos": "{path}/input/typos.csv".format(path=basePath),
    "gns_tbl": "gnsloc",
    "gns_error": "{path}/output/gns_error.txt".format(path=basePath),
}
