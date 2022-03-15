import mariadb
from decouple import config

dbpass = config('dbPass')
userToken = config('userToken')
hostToken = config('hostToken')
portToken = config('portToken')
dbname = config('dbname')

mydb = mariadb.connect(
        user=userToken,
        password=dbpass,
        host=hostToken,
        port=int(portToken),
        database=dbname)

db = mydb.cursor()