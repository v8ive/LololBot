import mariadb
from decouple import config

dbUser = config('dbUser')
dbPass = config('dbPass')
dbHost = config('dbHost')
dbPort = config('dbPort')
dbName = config('dbName')

mydb = mariadb.connect(
        user=dbUser,
        password=dbPass,
        host=dbHost,
        port=int(dbPort),
        database=dbName)

db = mydb.cursor()