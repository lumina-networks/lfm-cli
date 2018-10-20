Brocade Flow Manager Client library
===================================

Usage
-----

The Flow Manager client can be used as either library for packages
wishing to more easily access the Lumina Flow Manager functions or can
also be used as a command line interface tool to display LFM
information.

::

    lfm --help

Installation
------------

This library needs to be packaged into a source distribution and then
copied into a location that allows one of the packages that use it to
include it (i.e. on a web server like nginx).

Creating the source distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Need to do the following to create source distribution

1. Run the following command to make a source distribution

::

    $ make sdist

2. Copy the resulting distribution to a web server

::

    $ cd dist
    $ scp lfm-cli-2.0.0.tar.gz <webserver>:/web/dir

Running the tests
~~~~~~~~~~~~~~~~~

tests can be run on the package to ensure nothing has been broken

::

    $ make test