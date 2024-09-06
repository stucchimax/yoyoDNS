
from fastapi import FastAPI, HTTPException, Request

import os
import sqlite3

app = FastAPI()

@app.get("/")
async def main(request: Request):
    return("Hello World")

@app.get('/get_referer')
async def referer(request: Request):
    address = request.headers.get('referer')
    return address

@app.get['/uuid/{dbase}/{uuid}']
async def uuid_check(request: Request, dbase, uuid):
    
    query = f"SELECT * from queries WHERE uuid=\"{uuid}\""

    if os.path.isfile(f"{dbase}.sql"):
        con = sqlite3.connect(f'{dbase}.sql', check_same_thread=False)
        res = con.execute(query)

        entries = res.fetchall()

        con.close()

        return entries
    else:
        raise HTTPException(status_code=404, detail="Database not found") 

@app.get['/dbase/{dbase}']
async def dbase_create(request: Request, dbase):

    con = sqlite3.connect(f'{dbase}.sql', check_same_thread=False)

    query = "CREATE TABLE queries (uuid VARCHAR, ip_address VARCHAR, query_timestamp INTEGER, query_asn INTEGER, query_as_name VARCHAR, query_location VARCHAR)"

    con.execute(query)

    con.commit()

    con.close()

    return("Database created")



    

