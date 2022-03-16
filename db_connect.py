import sqlite3 as mysql
from decouple import config

mydb = mysql.connect('./db/main.db')

db = mydb.cursor()