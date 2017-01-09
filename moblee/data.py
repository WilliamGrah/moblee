import sqlite3


def get(filter):
    conn = sqlite3.connect('stackdata.db')
    c = conn.cursor()
    c.execute("SELECT * FROM stackdata {filter}".format(filter=filter))
    data = c.fetchall()
    c.close()
    return data


def create(data):
    conn = sqlite3.connect('stackdata.db')
    c = conn.cursor()
    c.execute(
        'INSERT INTO stackdata VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
        (
            data["question_id"], data["title"], data["owner_name"],
            data["score"], data["creation_date"], data["link"],
            data["is_answered"], data["last_update"]
        )
    )
    conn.commit()
    c.close()


def clean():
    conn = sqlite3.connect('stackdata.db')
    c = conn.cursor()
    c.execute('DELETE FROM stackdata')
    conn.commit()
    c.close()
