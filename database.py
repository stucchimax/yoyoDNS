#!/usr/bin/env python3

import sqlite3

con = sqlite3.connect('db.sql')

query = "CREATE TABLE measurements (uuid VARCHAR, asn INTEGER, timestamp INTEGER, measurement_id INTEGER, country VARCHAR, probe_id INTEGER, af INTEGER);"

con.execute(query)

query = "CREATE TABLE queries (uuid VARCHAR, ip_address VARCHAR, timestamp INTEGER)"

con.execute(query)

con.commit()

con.close()
