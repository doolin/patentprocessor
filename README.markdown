# Python scripts for disambiguating patent data

The following collection of scripts performs pre- and
post-processing on patent data as part of the patent
inventor disambiguation process.

## Contributing to the Patent Processor Project

Pull requests are welcome. Here are a few pointers which will make everything easier:

* Small, tightly constrained commits.
* New files should be in their own commit, and committed before they are used in subsequent commits.
* Commits should tell a story in a logical sequence. It should be possible to understand the gist
  of the development just from reading the commits (hard, but worthwhile goal).
* The ideal commit:
    * Unit (or similar) test for a single functionality.
    * Implementation to pass the unit test.
    * Documentation (the "why") of the function/method in the appropriate location (platform dependent).
    * 0 or 1 use of the new functionality in production.
    * Further uses of functionality should go in future commits.
* Formatting updates, code cleanup and renaming should go into independent commits.
* Testing scripts, including unit tests, integration tests and functional tests go in the `test` directory.
* Code which does work goes in the lib directory.
* Code which provides a workflow (i.e., processing patents or building necessary
  infrastructure) goes in the top level directory. In the future, much of this code may
  be put into a `bin` directory.
* Test code should follow the pattern `test/test_libfile.py`. This pattern may change in
  the future, whence this documentation will change at that time.


## Processing patents

`preprocess.sh` to get started.
