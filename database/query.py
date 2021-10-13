import sqlite3

conn = sqlite3.connect(
    'fc_management.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

c = conn.cursor()
'''
c.execute("INSERT INTO permissions(name, entity) VALUES (?, ?)", [
            "create", "user"]
)

c.execute("INSERT INTO groups(name) VALUES (?)", [
            "admin"]
)

c.execute("INSERT INTO user_permission(user_id, permission_id) VALUES (?, ?)", [
            1, 1]
)

c.execute("INSERT INTO user_group(user_id, group_id) VALUES (?, ?)", [
            1, 1]
)

c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
            1, 1]
)'''

'''c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 12]
)

c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 13]
)
c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 18]
)
c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 19]
)
c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 24]
)
c.execute("INSERT INTO group_permission(group_id, permission_id) VALUES (?, ?)", [
    2, 25]
)'''

c.execute("INSERT INTO user_group(user_id, group_id) VALUES (?, ?)", [
    2, 4]
)

conn.commit()

conn.close()
