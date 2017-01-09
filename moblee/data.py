import sqlite3

def get(filter):
    conn = sqlite3.connect('stackdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stackdata {filter}".format(filter=filter))
    data = c.fetchall()
    c.close()
    return data

def clean():
    conn = sqlite3.connect('stackdata.db')
    c = conn.cursor()
    c.execute('DELETE FROM stackdata')
    conn.commit()
    c.close()