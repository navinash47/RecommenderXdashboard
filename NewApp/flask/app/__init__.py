from flask import Flask
# from flaskext.mysql import MySQL

app=Flask(__name__,static_folder="static")
# mysql = MySQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = '12345'
# app.config['MYSQL_DATABASE_DB'] = 'hospitals'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
from app import view