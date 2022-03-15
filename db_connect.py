import mysql.connector as mysql
from decouple import config

dbUser = config('dbUser')
dbPass = config('dbPass')
dbHost = config('dbHost')
dbPort = config('dbPort')
dbName = config('dbName')

mydb = mysql.connect(
        user=dbUser,
        password=dbPass,
        host=dbHost,
        port=int(dbPort),
        database=dbName)

db = mydb.cursor()