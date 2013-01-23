# Test suite for patent preprocessing

We're intending on conforming to PEP guidelines,
please note where implementation is not meeting
a relevant PEP.

## Running integration tests

The integration tests require two types of databases:

1. A set of sqlite databases located in the test directory as a result
   of a succesful parse, and
2. Databases `loctbl` and `NBER_asg` linked from elsewhere like so:
    * `ln -s /data/patentdata/NBER/NBER_asg .`
    * `ln -s /data/patentdata/location/loctbl.sqlite3/NBER_asg loctbl`

(Your links may be different.)


