#!/usr/bin/env python3

import ipinfo
import os
import sqlite3

from pprint import pprint

from dotenv import load_dotenv

load_dotenv()

def get_ip_details(ip_address):
    access_token = os.getenv("IPINFO_API_TOKEN")
    print(access_token)
    handler = ipinfo.getHandler(access_token)
    details = handler.getDetails(ip_address)

    pprint(details.all)
    
    org_data = details.org.split()

    asn = org_data.pop(0)
    
    delimiter = " "
    as_name = delimiter.join(org_data)

    #print(asn)
    #print(as_name)

    location = "{},{}".format(details.longitude, details.latitude)
    return(asn, as_name, location)


def main():
    
    con = sqlite3.connect('db.sql')

    query = "SELECT * FROM queries"

    res = con.execute(query)

    for entry in res.fetchall():

        #print(entry[1])

        ip_address = entry[1]

        asn, as_name, location = get_ip_details(ip_address)
        
        to_update = "UPDATE queries SET query_asn = '{}', query_as_name = '{}', query_location = '{}' WHERE uuid == '{}' AND ip_address = '{}'".format(asn, as_name, location, entry[0], ip_address)
        print(to_update) 
        con.execute(to_update)
        con.commit()

if __name__ == '__main__':
    main()
