import sqlite3 as sql

def get_main():

    mydb = sql.connect('./db/main.db')

    db = mydb.cursor()
    
    return db, mydb