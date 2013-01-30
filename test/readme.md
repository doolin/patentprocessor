# Test suite for patent preprocessing

We're intending on conforming to PEP guidelines,
please note where implementation is not meeting
a relevant PEP.

Currently (January 30, 2013), we're running unit tests and integration
tests. We do not have full coverage for unit tests. Unit tests are being
constructed as part of the refactoring process, and all new code should
be covered in unit tests.

Integration tests will run end-to-end on the parsing, cleaning and consolidation
phases, but the current data sets used in the integration tests are
incomplete. Further, the location handling does not work correctly, so
the integration test covering geocoding is broken by designed.

## Running unit tests

The unit tests are invoked automatically in the `./patenttest.sh`
script.

### PATENTROOT

Not having `PATENTROOT` set will produce this warning notice:

```sh
Processing test_parse_config.py file..
Cannot find PATENTROOT environment variable. Setting PATENTROOT to the
patentprocessor directory for the scope of this test. Use `export
PATENTROOT=/path/to/directory` to change
```

This is easy to silence: `$ export PATENTROOT=.`

You may want to export `PATENTROOT` in your shell initialization script
for convenience.


## Running integration tests

The integration tests require two types of databases:

1. A set of sqlite databases located in the test directory as a result
   of a succesful parse, and
2. Databases `loctbl` and `NBER_asg` linked from elsewhere like so:
    * `ln -s /data/patentdata/NBER/NBER_asg .`
    * `ln -s /data/patentdata/location/loctbl.sqlite3 loctbl`

(Your links may be different.)


