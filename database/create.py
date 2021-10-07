import sqlite3
conn = sqlite3.connect(
    'fc_manager.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

c = conn.cursor()

c.execute("""CREATE TABLE user (
    id PRIMARY KEY,
    name text,
    email text,
    password text,
    permission text
    )""")



conn.commit()

conn.close()
