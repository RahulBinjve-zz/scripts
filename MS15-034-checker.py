#!/usr/bin/env python

""" Just another MS15-034-checker script on the Internet. This can also be used 
for masscanning by importing and calling "scan()" with target as an argument. Results might
be "inclonclusive". Author takes no responsibility.
Details here - http://blog.beyondtrust.com/the-delicate-art-of-remote-checks-a-glance-into-ms15-034
and https://ma.ttias.be/remote-code-execution-via-http-request-in-iis-on-windows/

Author - c0dist
"""

import sys
import requests


def scan(target):
    range_header = {"Range":"bytes=0-18446744073709551615"}
    try:
        head = requests.head(target)
        if "IIS" in head.headers["server"]:
            print "[+] Target is an IIS Server."
            response = requests.get(target, headers=range_header)
            if response.status_code == 416:
                return "Probable"
    except Exception as e:
        print "[-] Error occured. %s" % str(e)
    
    return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python %s <target>" % sys.argv[0]
        sys.exit(1)
        
    target = sys.argv[1]
    print "[+] Is target vulnerable? - %s" % scan(target)
    