from .interface import UserRepositoryInterface
import sqlite3

config = {
        "db_name": "fc_manager.db"
    }

class UserRepository(UserRepositoryInterface):
    @property
    def repository(self) -> UserRepositoryInterface:
        return self.repository

    def connectDB(crud_function):
        def connect_function(*args, **kwargs):
            conn = sqlite3.connect(config["db_name"])
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            with conn:
                return crud_function(cur, *args, **kwargs)
        return connect_function

    #Common Query
    @connectDB
    def get_all(cur, table_name):
        cur.execute("SELECT * FROM {}".format(table_name))
        return cur.fetchall()

    @connectDB
    def get_one_by_id(cur, table_name, id):
        cur.execute("SELECT * FROM {} WHERE id = ?".format(table_name), (id,))
        return cur.fetchone()

    @connectDB
    def get_by(cur, table_name, conditions, order_by=None, many=True):
        placeholders = '=? AND '.join(conditions.keys())
        if order_by:
            order_sql = "ORDER BY ?"
        else:
            order_sql = ""
        sql = "SELECT * FROM {} where {}=? {}".format(
            table_name, placeholders, order_sql)
        values = [int(x) if isinstance(x, bool)
                  else x for x in conditions.values()]
        if order_by:
            values.append(order_by)
        cur.execute(sql, values)
        if many:
            return cur.fetchall()
        return cur.fetchone()

    @connectDB
    def insert(cur, table_name, items):
        print(1)
        columns = ', '.join(items.keys())
        placeholders = ', '.join('?' * len(items))
        sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
            table_name, columns, placeholders)
        values = [int(x) if isinstance(x, bool) else x for x in items.values()]
        cur.execute(sql, values)
        return cur.lastrowid

    @connectDB
    def insert_many(cur, table_name, items_list):
        for items in items_list:
            columns = ', '.join(items.keys())
            placeholders = ', '.join('?' * len(items))
            sql = 'INSERT INTO {} ({}) VALUES ({})'.format(
                table_name, columns, placeholders)
            values = [int(x) if isinstance(x, bool)
                      else x for x in items.values()]
            cur.execute(sql, values)

    @connectDB
    def delete_one_by_id(cur, table_name, id):
        cur.execute("DELETE FROM {} WHERE id = ?".format(table_name), (id,))

    @connectDB
    def update(cur, table_name, items, conditions):
        placeholders = '=?,'.join(items.keys())
        placeholders2 = '=? AND '.join(conditions.keys())
        sql = "UPDATE {} SET {}=? WHERE {}=?".format(
            table_name, placeholders, placeholders2)
        placeholders_value = list(items.values()) + list(conditions.values())
        values = [int(x) if isinstance(x, bool)
                  else x for x in placeholders_value]
        cur.execute(sql, values)

    @connectDB
    def read_permission(self, user_id):
        query = "SELECT {} FROM {} WHERE {}".format(
            "permission_id", "permission", "user.group_id=group_permission.group_id AND group_permission.permission_id ="
        )
    
    def create_sth():
        print("created!")
        return 1