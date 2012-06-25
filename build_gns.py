# International Country Files Geographic Names (GNS)
# http://earth-info.nga.mil/gns/html/gis_countryfiles.htm
# http://earth-info.nga.mil/gns/html/geonames_dd_dms_date_20120402.zip

import sys
import datetime, csv, os, re, sqlite3, unicodedata
sys.path.append("lib")
import SQLite
from locFunc import uniasc, cityctry
from fwork import *
from config import *

cc_iso = {'BD': 'BM', 'BF': 'BS', 'BG': 'BD', 'BA': 'BH', 'WA': 'NA', 'BC': 'BW', 'BL': 'BO', 'BN': 'BJ', 'BO': 'BY', 'BH': 'BZ', 'WI': 'EH', 'BK': 'BA', 'BU': 'BG', 'BP': 'SB', 'TP': 'ST', 'BX': 'BN', 'BY': 'BI', 'RP': 'PH', 'RS': 'RU', 'TL': 'TK', 'RM': 'MH', 'RI': 'RS', 'TK': 'TC', 'GV': 'GN', 'GG': 'GE', 'GB': 'GA', 'GA': 'GM', 'GM': 'DE', 'GK': 'GG', 'GJ': 'GD', 'SV': 'SJ', 'HO': 'HN', 'HA': 'HT', 'PS': 'PW', 'PP': 'PG', 'PU': 'GW', 'JA': 'JP', 'PC': 'PN', 'PA': 'PY', 'PO': 'PT', 'PM': 'PA', 'EN': 'EE', 'EI': 'IE', 'ZI': 'ZW', 'EK': 'GQ', 'ZA': 'ZM', 'EZ': 'CZ', 'AN': 'AD', 'ES': 'SV', 'UP': 'UA', 'MG': 'MN', 'MF': 'YT', 'MA': 'MG', 'MC': 'MO', 'MB': 'MQ', 'MO': 'MA', 'MN': 'MC', 'MI': 'MW', 'MH': 'MS', 'MJ': 'ME', 'MU': 'OM', 'MP': 'MU', 'UK': 'GB', 'VT': 'VA', 'FP': 'PF', 'FS': 'TF', 'FG': 'GF', 'NH': 'VU', 'NI': 'NG', 'NE': 'NU', 'NG': 'NE', 'NS': 'SR', 'NT': 'AN', 'NU': 'NI', 'CK': 'CC', 'CJ': 'KY', 'CI': 'CL', 'CH': 'CN', 'CN': 'KM', 'CB': 'KH', 'CG': 'CD', 'CF': 'CG', 'CE': 'LK', 'CD': 'TD', 'CS': 'CR', 'CW': 'CK', 'CT': 'CF', 'SZ': 'CH', 'SX': 'GS', 'SP': 'ES', 'SW': 'SE', 'KN': 'KP', 'SU': 'SD', 'ST': 'LC', 'KS': 'KR', 'KR': 'KI', 'SN': 'SG', 'KU': 'KW', 'KT': 'CX', 'SC': 'KN', 'SB': 'PM', 'SG': 'SN', 'SF': 'ZA', 'SE': 'SC', 'DO': 'DM', 'UV': 'BF', 'YM': 'YE', 'DA': 'DK', 'DR': 'DO', 'LG': 'LV', 'LE': 'LB', 'TX': 'TM', 'LO': 'SK', 'TT': 'TL', 'TU': 'TR', 'TS': 'TN', 'LH': 'LT', 'LI': 'LR', 'TN': 'TO', 'TO': 'TG', 'LT': 'LS', 'LS': 'LI', 'TI': 'TJ', 'TD': 'TT', 'AA': 'AW', 'AC': 'AG', 'IZ': 'IQ', 'AG': 'DZ', 'VI': 'VG', 'IS': 'IL', 'AJ': 'AZ', 'WZ': 'SZ', 'VM': 'VN', 'IV': 'CI', 'AS': 'AU', 'AU': 'AT', 'AV': 'AI', 'IC': 'IS'}
# TODO: What is this above?

errors = open(loc["gns_error"], "wb")

s = SQLite.SQLite(loc["db"], table=loc["gns_tbl"])
#s.conn.text_factory = "utf-8"
data = [x.split("\t") for x in open(loc["gns"], "rb")]
# TODO: The GNS file appears to be a tab-delimited file rather than CSV
s.c.executescript("""
    CREATE TABLE IF NOT EXISTS {table} ({schema})
    """.format(table=loc["gns_tbl"],
               schema=", ".join(data[0]))) #"""
s.index([u"RC", u"CC1", u"ADM1", u"CC2", u"SORT_NAME_RO"], unique=True)
# TODO: Unit-test new GNS header against existing GNS header
# WARNING: We are not handling unicode, especially Arabic
for d in data[1:]:
    try:
        s.c.execute("INSERT OR REPLACE INTO {table} VALUES ({ques})".format(
            table=loc["gns_tbl"], ques=", ".join(["?"]*len(d))), 
            [uniasc(x) for x in d])
    except Exception as e:
        # TODO: Log exceptions, especially Arabic
        print "FIXME:", "|".join(d)
        errors.write("FIXME: " + "|".join(d))

s.index(["RC"])
s.index(["CC1"])
s.index(["CC2"])
s.index(["ADM1"])
s.index(["FC"])
s.index(["SORT_NAME_RO", "CC1"])
s.index(["FULL_NAME_RO", "CC1"])
s.index(["FULL_NAME_ND_RO", "CC1"])
s.close()
