#!/usr/bin/env python
"""
This script will return a dictionary having Global and country rank of a domain,
fetched from Alexa. This does not use the API, but the instead dirtily parses the 
HTML response. Might break in future.

Author - c0dist
TODO: Adding comments.
"""
import sys
import requests
from bs4 import BeautifulSoup as bs

def get_rank(domain_to_query):
    result = {'Global':''}
    url = "http://www.alexa.com/siteinfo/" + domain_to_query
    page = requests.get(url).text
    soup = bs(page)
    for span in soup.find_all('span'):
        if span.has_attr("class"):
            if "globleRank" in span["class"]:
                for strong in span.find_all("strong"):
                    if strong.has_attr("class"):
                        if "metrics-data" in strong["class"]:
                            result['Global'] = strong.text
            # Extracting CountryRank
            if "countryRank" in span["class"]:
                image = span.find_all("img")
                for img in image:
                    if img.has_attr("title"):
                        country = img["title"].replace(" Flag", "")
                for strong in span.find_all("strong"):
                    if strong.has_attr("class"):
                        if "metrics-data" in strong["class"]:
                            result[country] = strong.text
    return result

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "Usage: python alexa.py <domain.com>"
        sys.exit(1)
    print get_rank(sys.argv[1])
