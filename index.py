from bottle import *
import pymysql

@error(405)
def error405(error):
    return "Action not allowed<br>" \
           "Click <a href='/'>here</a> to sign up or <a href='/login'>here</a> to login "

@route("/")
def index():
    return template("forsida.tpl")

@route("/signup", method="POST")
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

@route("/login")
def login():
    return template("login.tpl")

@route("/check", method="POST")
def check():
    connect = pymysql.connect(user="1612002390", passwd="mypassword", host="tsuts.tskoli.is", port=3306,database="1612002390_veflokaverkefni")
    username = request.forms.get("username")
    passwd = request.forms.get("passwd")
    with connect.cursor() as cursor:
        sql = "select * from users where username=%s and passwd=%s;"
        if cursor.execute(sql, (username, passwd)):
            return "Welcome: " + username + "<br>" \
                   "Click <a href='/forsida'>here</a> to shop"
        else:
            return "Login failed<br>" \
                   "Click <a href='/login'>here</a> to go back to login"

@route("/forsida")
def forsida():
    connect = pymysql.connect(user="1612002390", passwd="mypassword", host="tsuts.tskoli.is", port=3306,database="1612002390_veflokaverkefni")
    with connect.cursor() as cursor:
        sql = "select * from bilar"
        cursor.execute(sql)
        utkoma = cursor.fetchall()
        for i in utkoma:
            id = i[0]
            name = i[1]
            year = i[2]
            mora = i[3]
            uorn = i[4]
            price = i[5]

    return template("bilar.tpl")



@route('/images/<filename:re:.*\.jpg>')
def image(filename):
    return static_file(filename, root='./images', mimetype='image/jpg')


run(host='localhost', port=8080)