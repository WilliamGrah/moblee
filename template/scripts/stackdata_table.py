import sqlite3
db = sqlite3.connect('stackdata.db')
db.execute("CREATE TABLE stackdata (question_id integer PRIMARY KEY,title char(250),owner_name char(100) NOT NULL,	score integer NOT NULL,	creation_date datetime NOT NULL,link text NOT NULL,is_answered boolean NOT NULL,	last_update datetime NOT NULL)");
db.commit()
