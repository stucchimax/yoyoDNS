
from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/")
def main(request: Request):
    return("Hello World")

@app.get('/get_referer')
def referer(request: Request):
    address = request.headers.get('referer')
    return address

@app.get['/uuid/{dbase}/{uuid}']
def uuid(request: Request, dbase, uuid):
    
    query = f"SELECT * from queries WHERE uuid=\"{uuid}\""

    con = sqlite3.connect(f'{dbase}.sql', check_same_thread=False)
    res = con.execute(query)

    entries = res.fetchall()

    con.close()

    return entries

