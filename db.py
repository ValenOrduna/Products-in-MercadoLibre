import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

connection = pymysql.connect(
    host=os.getenv('HOST'),
    user='u905721742_valenordu',
    password=os.getenv('PASSWORD'),
    database=os.getenv('DATABASE'),
    cursorclass=pymysql.cursors.DictCursor
)

connection.close()
