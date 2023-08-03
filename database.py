#!/usr/bin/env python3

import sqlite3

con = sqlite3.connect('db.sql')

query = "CREATE TABLE measurements (uuid VARCHAR, msm_asn INTEGER, msm_timestamp INTEGER, measurement_id INTEGER, country VARCHAR, probe_id INTEGER, af INTEGER);"

con.execute(query)

query = "CREATE TABLE queries (uuid VARCHAR, ip_address VARCHAR, query_timestamp INTEGER, query_asn INTEGER, query_as_name VARCHAR, query_location VARCHAR)"

con.execute(query)

con.commit()

con.close()
