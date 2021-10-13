import sqlite3

conn = sqlite3.connect(
    'fc_management.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

c = conn.cursor()

c.execute("""CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    password TEXT
)""")

c.execute("""CREATE TABLE groups (
    id INTEGER PRIMARY KEY,
    name TEXT
    )""")

c.execute("""CREATE TABLE permissions (
    id INTEGER PRIMARY KEY,
    name TEXT,
    entity TEXT
    )""")

c.execute("""CREATE TABLE user_group (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    group_id INTEGER
    )""")

c.execute("""CREATE TABLE user_permission (
    id INTEGER PRIMARY KEY,
    user_id INTEGER,
    permission_id INTEGER
    )""")

c.execute("""CREATE TABLE group_permission (
    id INTEGER PRIMARY KEY,
    group_id INTEGER,
    permission_id INTEGER
    )""")

c.execute("""CREATE TABLE league (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER
    )""")

c.execute("""CREATE TABLE football_club (
    id INTEGER PRIMARY KEY,
    name TEXT,
    quantity INTEGER
    )""")

c.execute("""CREATE TABLE player (
    id INTEGER PRIMARY KEY,
    name TEXT,
    fc_id INTEGER
    )""")

c.execute("""CREATE TABLE league_fc (
    id INTEGER PRIMARY KEY,
    league_id INTEGER,
    fc_id INTEGER
    )""")

conn.commit()

conn.close()
