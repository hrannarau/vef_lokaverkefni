from bottle import *
import pymysql
from beaker.middleware import SessionMiddleware

@error(405)
def error405(error):
    return "Action not allowed<br>" \
           "Click <a href='/'>here</a> to sign up or <a href='/login'>here</a> to login "

@route("/")
def index():
    response.set_cookie("name","",expires=0)
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
            response.set_cookie("name",username)
            return "Welcome: " + username + "<br>" \
                   "Click <a href='/forsida'>here</a> to shop"
        else:
            return "Login failed<br>" \
                   "Click <a href='/login'>here</a> to go back to login"

@route("/forsida")
def forsida():
    return template("bilar.tpl")

shoppingCart = []
@route("/add/<item>")
def add(item):
    if item not in shoppingCart:
        shoppingCart.append(item)
        redirect("/forsida")
    else:
        return "Would you like to add another ",item," to your cart?"



@route("/cart")
def cart():
    if request.get_cookie("name"):
        return "Welcome back ",request.get_cookie("name"),\
               ". Nice to see you again<br>", \
               "Your cart: ",shoppingCart,"<br>" \
               "Click <a href='/delete'>here</a> to delete items from cart"

    else:
        return "Hello there! Would you like to <a href='/login'>login</a>?<br>" \
               "Don't have an account?<br>" \
               "Your cart: ",shoppingCart,"<br>" \
               "Click <a href='/'>here</a> to create a new account.<br>" \
               "Click <a href='/delete'>here</a> to delete items from cart"

@route("/delete")
def delete():
    session = request.environ.get('beaker.session')
    session.delete()
    redirect("/forsida")

@route('/images/<filename:re:.*\.jpg>')
def image(filename):
    return static_file(filename, root='./images', mimetype='image/jpg')

@route('/css/<filename:re:.*\.css>')
def css(filename):
       return static_file(filename, root='./css')


run(host='localhost', port=8080)