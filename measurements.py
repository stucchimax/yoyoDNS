#!/usr/bin/env python3

import argparse
import os
import requests
import sqlite3
import uuid

from datetime import datetime

from time import sleep

from ripe.atlas.cousteau import AtlasCreateRequest, AtlasSource, Traceroute, Dns

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

from dotenv import load_dotenv

retry_strategy = Retry(
    total=8,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["HEAD", "GET", "OPTIONS"]
)

load_dotenv()

atlas_api_key = os.getenv("ATLAS_API_KEY")

parser = argparse.ArgumentParser(description='Generate measurements to understand where DNS resolvers are in a country or ASN')

parser.add_argument("country", help="the country (in ISO 2-letter format)")

args = parser.parse_args()


# Get all the ASNs in the country

def asn_list():
    url = "https://ftp.ripe.net/ripe/asnames/asn.txt"

    q = requests.Session()

    p = q.get(url, timeout=20)

    asns = {}

    for line in p.iter_lines():
        split_line = line.decode().split(", ")

        try:
            country = split_line[1]
            split_line.pop(1)
        except:
            country = "ZZ"

        as_details = split_line[0].split()

        asn = as_details[0]

        as_details.pop(0)

        try:
            as_name = ' '.join(as_details)
        except:
            as_name = "None/Reserved"

        #print("AS {} has name '{}' and country {}".format(asn, as_name, country))

        asns[asn] = {"country": country, "as_name": as_name}

    return(asns)

asns = asn_list()

for asn in asns:

    if asns[asn]['country'] == args.country:
    
        # Get all the probes in any ASN

        url = "https://atlas.ripe.net/api/v2/probes/?asn={}&status=1".format(asn)

        r = requests.Session()

        s = r.get(url, timeout=20)

        probes = s.json()

        if probes['count'] > 0:
            for probe in probes['results']:     
                dt = datetime.now()
                ts = datetime.timestamp(dt)
                done = False
                if probe['asn_v4'] is not None:
                    host_uuid = uuid.uuid4()
                    print("Host for probe {} in AS{} would be: {}.valid.keyrollover.ch".format(probe['id'],probe['asn_v4'], host_uuid))
                    source = AtlasSource(
                            requested=1,
                            type="probes",
                            value=probe['id']
                            )
                    dns = Dns(
                            af=4,
                            description="yoyoDNS test measurement",
                            query_class="IN",
                            query_type="A",
                            query_argument="{}.valid.keyrollover.ch".format(host_uuid),
                            use_probe_resolver=True
                            )
                    atlas_request = AtlasCreateRequest(
                            key=atlas_api_key,
                            measurements=[dns],
                            sources=[source],
                            is_oneoff=True
                    )
                    while done == False:
                        (is_success, response) = atlas_request.create()
                        if 'measurements' in response:
                            print("Measurement accepted, with id: {}".format(response['measurements'][0]))
                            done = True

                            query = "INSERT INTO measurements values('{}', '{}', '{}', '{}', '{}','{}','4')".format(host_uuid, asn, ts, response['measurements'][0], args.country, probe['id'])
                    
                            con = sqlite3.connect('db.sql', check_same_thread=False)
                            con.execute(query)
                            con.commit()
                            con.close()

                        else:
                            print("Cycling, we need to wait")
                            print(response)
                            sleep(2)

                done = False
                if probe['asn_v6'] is not None:
                    host_uuid = uuid.uuid4()
                    print("Host for probe {} in AS{} would be: {}.valid.keyrollover.ch".format(probe['id'],probe['asn_v6'], host_uuid))
                    source = AtlasSource(
                            requested=1,
                            type="probes",
                            value=probe['id']
                            )
                    dns = Dns(
                            af=6,
                            description="yoyoDNS test measurement",
                            query_class="IN",
                            query_type="A",
                            query_argument="{}.valid.keyrollover.ch".format(host_uuid),
                            use_probe_resolver=True
                            )
                    atlas_request = AtlasCreateRequest(
                            key=atlas_api_key,
                            measurements=[dns],
                            sources=[source],
                            is_oneoff=True
                    )
                    
                    while done == False:
                        (is_success, response) = atlas_request.create()
                        if 'measurements' in response:
                            print("Measurement accepted, with id: {}".format(response['measurements'][0]))
                            done = True

                            query = "INSERT INTO measurements values('{}', '{}', '{}', '{}', '{}', '{}', '6')".format(host_uuid, asn, ts, response['measurements'][0], args.country, probe['id'])
                    
                            con = sqlite3.connect('db.sql', check_same_thread=False)
                            con.execute(query)
                            con.commit()
                            con.close()

                        else:
                            print("Cycling, we need to wait")
                            print(response)
                            sleep(2)


# Generate a measurement for it

# Save data in DB

