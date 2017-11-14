from bottle import *
import pymysql

@route("/")
def index():
    return template("forsida.tpl")

@route("/signup")
def signup():
    connect = pymysql.connect(user="1612002390", passwd="mypassword", host="tsuts.tskoli.is", port=3306,database="1612002390_veflokaverkefni")

    username = request.forms.get("name")
    email = request.forms.get("email")
    password = request.forms.get("passwd")

    with connect.cursor() as cursor:
        try:
            sql = "INSERT INTO users (username,email,passwd) VALUES (%s,%s,%s)"
            cursor.execute(sql,(username,email,password))
            connect.commit()
            return "Thank you for signing up<br>" \
                   "Your username is:" + username+\
                   "<br>Click <a href='/login'>here</a> to login"
        except pymysql.err.IntegrityError:
            return "This username is already taken :(<br>" \
                   "<a href='/'>Click here to go back</a>"

run(host='localhost', port=8080)