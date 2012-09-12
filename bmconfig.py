
# This needs to be extracted from an environment variable
# or something.
basePath = "/home/doolin/src/patentbenchmarks"

# benchmarks dictionary, which files are which..

loc = {
    "db": "{path}/output/loctbl.sqlite3".format(path=basePath),
    "gns": "{path}/input/geonames.txt".format(path=basePath),
    "us_tbl": "congdist",
    "gns_tbl": "gnsloc",
    "mtch_tbl": "matchloc",
    "s3_dir": "{path}/output/s3".format(path=basePath),
}
