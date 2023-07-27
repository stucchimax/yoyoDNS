# yoyoDNS

A testing suite for DNS Resolvers in an ASN or a country.

This set of scripts works with two separate parts: one which sets up RIPE Atlas DNS measurements, and the other one running a DNS Server to log all the resulting queries and the source IP address(es) of the resolver(s) in a database.

The queries performed are all under one single subdomain (in this case, valid.keyrollover.ch), and are constituted of unique entries, generated with UUIDs (such as 16fd2706-8baf-433b-82eb-8c7fada847da.valid.keyrollover.ch.).  This allows us to identify from which resolver IP a query is coming from in a given ASN.

The two processes save information in a shared SQLite DB.

## Setting up

You need to generate a RIPE Atlas API Key and grant it the "Create new measurement" capability, then put the key in a __.env__ file with the following format:

```shell
ATLAS_API_KEY=12345678910
```

After this, you need to create a python _virtualenv_:

```shell
python3 -m venv venv
```

and intall the required libraries

```shell
source ./venv/bin/activate
pip3 install -U -r requirements.txt
```

Before we start, we need to create the database:

```shell
python3 ./database.py
```



## Running the tests

There are two separate scripts to run, one running the DNS Server, and the other one generating the measurements.

### DNS Server

You need to have a dedicated subdomain with your own delegation to the server running this configuration.  An example configuration file - _test.com.zone_ - is provided, which contains configuration for our own test domain and subdomain, _valid.keyrollover.ch_.

Once you have delegation set up, you can run the DNS Server as follows:

```shell
python3 ./dns-server.py
```

It will print out a message telling you it is running.  By default, it binds on all the IPv4 and IPv6 addresses on your server.  This code is taken straight from the following github repository: https://github.com/nimjim/SimpleAuthDNS.

### Measurements

You can now run the measurements:

```shell
python3 ./measurements.py $COUNTRY
```

where $COUNTRY is the ISO-2 country code for the country for which you want to run measurements.

# Results

Once finished, you can find the results in the db.sql SQLite database, in the "measurements" table.

# Contacts

For any question, don't hesitate to either open an issue on GitHub, or send an email to stucchi@isoc.org and siddiqui@isoc.org.