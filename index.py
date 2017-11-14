from bottle import *
import pymysql

@route("/")
def index:
    