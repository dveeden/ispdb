
ISPDB
=====

Python Library for the Mozilla ISPDB

The original package is available on:
https://pypi.python.org/pypi/ispdb/

Known Issues
============

The Mozilla servers use TLS with SNI, but this is not supported by the
requests library which is used by this package. The requests package
used the python SSL libraries. This is only a limitation on Python 2.x
as the SSL library on Python 3.x does support SNI.

Only the Mozilla ISPDB is used, the autoconfig.domain.tld URL is not
tried and the well-known URI is also not tried. So only the ISPDB @ 
Mozilla works.

Other documentation
===================

Documentation for the specifications can be found on
https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration
