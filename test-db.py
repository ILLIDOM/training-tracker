import sqlite3
import os

basedir = os.path.abspath(os.path.dirname(__file__))

def main():
    database = os.path.join(basedir, "training.db")
    conn = sqlite3.connect(database)

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM 'set'")

        rows = cur.fetchall()

        for row in rows:
                print(row)

if __name__ == '__main__':
    main()