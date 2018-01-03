#!/bin/env python
#
#
from urllib2 import Request, urlopen, URLError

UDTOP="http://169.254.169.254/latest/meta-data"
LOCAL="http://dev.racf.bnl.gov/dist/"

def get_metadata():
    print("Getting metadata...")

    req = Request(UDTOP)
    try:
        response = urlopen(req)
        print(response.read())
    except URLError, e:
        if hasattr(e, 'reason'):
            print( 'We failed to reach a server.')
            print( 'Reason: ', e.reason )
        elif hasattr(e, 'code'):
            print( 'The server couldn\'t fulfill the request.' )
            print( 'Error code: ', e.code )
            


if __name__ == "__main__":
    get_metadata()
