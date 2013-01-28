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

cc_iso = {'BD': 'BM', 'BF': 'BS', 'BG': 'BD', 'BA': 'BH', 'WA': 'NA',
          'BC': 'BW', 'BL': 'BO', 'BN': 'BJ', 'BO': 'BY', 'BH': 'BZ',
          'WI': 'EH', 'BK': 'BA', 'BU': 'BG', 'BP': 'SB', 'TP': 'ST',
          'BX': 'BN', 'BY': 'BI', 'RP': 'PH', 'RS': 'RU', 'TL': 'TK',
          'RM': 'MH', 'RI': 'RS', 'TK': 'TC', 'GV': 'GN', 'GG': 'GE',
          'GB': 'GA', 'GA': 'GM', 'GM': 'DE', 'GK': 'GG', 'GJ': 'GD',
          'SV': 'SJ', 'HO': 'HN', 'HA': 'HT', 'PS': 'PW', 'PP': 'PG',
          'PU': 'GW', 'JA': 'JP', 'PC': 'PN', 'PA': 'PY', 'PO': 'PT',
          'PM': 'PA', 'EN': 'EE', 'EI': 'IE', 'ZI': 'ZW', 'EK': 'GQ',
          'ZA': 'ZM', 'EZ': 'CZ', 'AN': 'AD', 'ES': 'SV', 'UP': 'UA',
          'MG': 'MN', 'MF': 'YT', 'MA': 'MG', 'MC': 'MO', 'MB': 'MQ',
          'MO': 'MA', 'MN': 'MC', 'MI': 'MW', 'MH': 'MS', 'MJ': 'ME',
          'MU': 'OM', 'MP': 'MU', 'UK': 'GB', 'VT': 'VA', 'FP': 'PF',
          'FS': 'TF', 'FG': 'GF', 'NH': 'VU', 'NI': 'NG', 'NE': 'NU',
          'NG': 'NE', 'NS': 'SR', 'NT': 'AN', 'NU': 'NI', 'CK': 'CC',
          'CJ': 'KY', 'CI': 'CL', 'CH': 'CN', 'CN': 'KM', 'CB': 'KH',
          'CG': 'CD', 'CF': 'CG', 'CE': 'LK', 'CD': 'TD', 'CS': 'CR',
          'CW': 'CK', 'CT': 'CF', 'SZ': 'CH', 'SX': 'GS', 'SP': 'ES',
          'SW': 'SE', 'KN': 'KP', 'SU': 'SD', 'ST': 'LC', 'KS': 'KR',
          'KR': 'KI', 'SN': 'SG', 'KU': 'KW', 'KT': 'CX', 'SC': 'KN',
          'SB': 'PM', 'SG': 'SN', 'SF': 'ZA', 'SE': 'SC', 'DO': 'DM',
          'UV': 'BF', 'YM': 'YE', 'DA': 'DK', 'DR': 'DO', 'LG': 'LV',
          'LE': 'LB', 'TX': 'TM', 'LO': 'SK', 'TT': 'TL', 'TU': 'TR',
          'TS': 'TN', 'LH': 'LT', 'LI': 'LR', 'TN': 'TO', 'TO': 'TG',
          'LT': 'LS', 'LS': 'LI', 'TI': 'TJ', 'TD': 'TT', 'AA': 'AW',
          'AC': 'AG', 'IZ': 'IQ', 'AG': 'DZ', 'VI': 'VG', 'IS': 'IL',
          'AJ': 'AZ', 'WZ': 'SZ', 'VM': 'VN', 'IV': 'CI', 'AS': 'AU',
          'AU': 'AT', 'AV': 'AI', 'IC': 'IS'}

# TODO: This recodes Countries.
#   Add back in (look at line 93 of historical)
#   https://github.com/laironald/patentprocessor/blob/69d6ec00512907932120ff8d8c3406ae007e899a/build_gns.py#L93

s = SQLite.SQLite(loc["db"], tbl=loc["gns_tbl"])
#s.conn.text_factory = "utf-8"
s.addSQL(loc["gns"], delimiter="\t", tbl=loc["gns_tbl"], errlog=loc["gns_error"], header=True)
s.index(["RC"])
s.index(["CC1"])
s.index(["CC2"])
s.index(["ADM1"])
s.index(["FC"])
s.index(["SORT_NAME_RO", "CC1"])
s.index(["FULL_NAME_RO", "CC1"])
s.index(["FULL_NAME_ND_RO", "CC1"])
s.close()
