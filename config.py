basePath = "/home/ronlai/patent"

loc = {
    "db": "{path}/output/loctbl.sqlite3".format(path=basePath),
    "gns": "{path}/input/geonames.txt".format(path=basePath),
    "nat": "{path}/input/natfile.txt".format(path=basePath),
    "typo": "{path}/input/typos.csv".format(path=basePath),
    "usloc": "{path}/input/natfile.txt".format(path=basePath),
    "us_db": "{path}/input/CD_ZIP.sqlite3".format(path=basePath),
    "typos": "{path}/input/typos.csv".format(path=basePath),
    "nat": "{path}/input/natfile.txt".format(path=basePath),
    "us_tbl": "congdistZip",
    "nat_tbl": "usloc",
    "gns_tbl": "gnsloc",
    "gns_error": "{path}/output/gns_error.txt".format(path=basePath),
    "nat_error": "{path}/output/nat_error.txt".format(path=basePath),
}
