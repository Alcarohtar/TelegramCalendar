import mariadb
import sys
import Calendario_privateInfo


def connect_to_database():
    '''This function is useful to connect to our database
    Modify Calendario_privateInfo.py file to add the following input'''
    try:
        conn = mariadb.connect(
        user=Calendario_privateInfo.user,
        password=Calendario_privateInfo.password,
        host=Calendario_privateInfo.host,
        port=Calendario_privateInfo.port,
        database=Calendario_privateInfo.database)
        #print("Connection to DB is OK")
        cur = conn.cursor()
        return cur, conn

    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

def execute_query(cur, conn, query, data):
    '''This function execute the queries given by other functions'''
    cur.execute(query,data)
    conn.commit()

def add_row(cur, conn, datetime, description, start_time=0, end_time=0):
    '''This function is used to add a row to table'''
    try:
        query="INSERT INTO calendario_famiglia (data, descrizione, ora_inizio, ora_fine) VALUES (?, ?, ?, ?)"
        data=(datetime, description, start_time, end_time)
        execute_query(cur, conn, query, data)
    except mariadb.Error as e: 
        print(f"Error: {e}")

def remove_row(cur, conn, id):
    '''This function is used to remove a row from the table'''
    try:
        query="DELETE FROM calendario_famiglia WHERE id=%s"
        data=(id,)
        execute_query(cur, conn, query, data)
    except mariadb.Error as e: 
        print(f"Error: {e}")

def show_table(cur, conn):
    '''This function is used to show the total row in table'''
    try:
        cur.execute("SELECT * FROM calendario_famiglia ORDER BY data")
        #for i in cur:
        #    print(i)
        return cur
    except mariadb.Error as e: 
        print(f"Error: {e}")

def show_data(cur, conn, calend):
    '''This function is used to show the data column in table'''
    try:
        query="SELECT data FROM calend=%s"
        data=(calend,)
        execute_query(cur, conn, query, data)
        #for i in cur:
        #    print(i)
        return cur
    except mariadb.Error as e: 
        print(f"Error: {e}")

def reset_id_counter(cur, conn):
    '''This function is useful to reset the id increment, so when another row 
    has added, it take the lower id available'''
    try:
        cur.execute("ALTER TABLE calendario_famiglia MODIFY id INTEGER NOT NULL")
        cur.execute("ALTER TABLE calendario_famiglia MODIFY id INTEGER NOT NULL AUTO_INCREMENT")
        #for i in cur:
        #    print(i)
        return cur
    except mariadb.Error as e: 
        print(f"Error: {e}")


def delete_all_rows(cur,conn):
    '''Delete all rows in table, but table is not deleted'''
    try:
        cur.execute("DELETE FROM calendario_famiglia")
        #for i in cur:
        #    print(i)
        return cur
    except mariadb.Error as e: 
        print(f"Error: {e}")


