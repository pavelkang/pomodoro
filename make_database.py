import sqlite3 as lite
import sys

sales = {
    ("Kai", 100),
    ("Jef", 100),
    ("Peter", 100),
}

con = lite.connect('database.db')
with con:
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS reps")
    cur.execute("CREATE TABLE reps(rep_name TEXT, amount INT)")
    cur.executemany("INSERT INTO reps VALUES(?,?)", sales)
