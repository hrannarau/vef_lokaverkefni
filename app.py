import os
from bottle import *
import pymysql

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
    response.set_cookie("name", "", expires=0)
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

Cart = []
@route("/add/<item>")
def add(item):
        Cart.append(item)
        redirect("/forsida")



@route("/cart")
def cart():
    shoppingCart = ["<br>"]
    for i in Cart:
        if i == "golf2000":
            shoppingCart.append("VW Golf")
        elif i == "ford2006":
            shoppingCart.append("Ford Escape Limited")
        elif i == "toyota1994":
            shoppingCart.append("Toyota Corolla")
        elif i == "toyota2001":
            shoppingCart.append("Toyota Rav")
        elif i == "mazda2004":
            shoppingCart.append("Mazda 6")
        elif i == "chevrolet2011":
            shoppingCart.append("Chevrolet Cruze")
        elif i == "renault2004":
            shoppingCart.append("Renault Mégane")
        elif i == "honda2004":
            shoppingCart.append("Honda Accord")
    cart = '<br>'.join(shoppingCart)
    if request.get_cookie("name"):
        return "Welcome back ",request.get_cookie("name"),". Nice to see you again<br><br>" \
               "---------------------------------------------------<br>"\
               "YOUR CART",cart,"<br><br>" \
               "        <a href='/checkout'>-----CHECKOUT-----</a><br>" \
               "---------------------------------------------------<br><br>"\
               "Click <a href='/delete'>here</a> to delete items from cart" \
               "Click <a href='/forsida'>here</a> to go back to the homepage"

    else:
        return "Hello there! Would you like to <a href='/login'>login</a>?<br>" \
               "Don't have an account?<br>"\
               "Click <a href='/'>here</a> to create a new account.<br><br>" \
               "---------------------------------------------------<br>" \
               "YOUR CART", cart, "<br><br>" \
               "        <a href='/checkout'>-----CHECKOUT-----</a><br>" \
               "---------------------------------------------------<br>" \
               "Click <a href='/delete'>here</a> to delete items from cart<br><br>" \
               "Click <a href='/forsida'>here</a> to go back to the homepage"

@route("/delete")
def delete():
    Cart.clear()
    redirect("/forsida")

@route("/checkout")
def checkout():
    shoppingCart = ["<br>"]
    for i in Cart:
        if i == "golf2000":
            shoppingCart.append("VW Golf")
        elif i == "ford2006":
            shoppingCart.append("Ford Escape Limited")
        elif i == "toyota1994":
            shoppingCart.append("Toyota Corolla")
        elif i == "toyota2001":
            shoppingCart.append("Toyota Rav")
        elif i == "mazda2004":
            shoppingCart.append("Mazda 6")
        elif i == "chevrolet2011":
            shoppingCart.append("Chevrolet Cruze")
        elif i == "renault2004":
            shoppingCart.append("Renault Mégane")
        elif i == "honda2004":
            shoppingCart.append("Honda Accord")
    cart = '<br>'.join(shoppingCart)

    connect = pymysql.connect(user="1612002390", passwd="mypassword", host="tsuts.tskoli.is", port=3306,database="1612002390_veflokaverkefni")
    upphaed = 0
    upphaedListi = []
    with connect.cursor() as cursor:
        sql = "select price from bilar where name = %s"
        for i in shoppingCart:
            if cursor.execute(sql,(i)):
                results = cursor.fetchone()
                utkoma = results[0]
                upphaedListi.append(utkoma)

    for i in upphaedListi:
        upphaed = upphaed + i
    return "----------CHECKOUT----------   <a href ='/forsida'>Home</a>  <a href='/cart'>Cart</a>", \
           cart, "<br><br>" \
                 "Total cost: ", str(upphaed), " ISK<br><br>" \
           "<a href='confirm'>Confirm order</a>"

@route("/confirm")
def confirm():
    if request.get_cookie("name"):
        return "Order has been confirmed.<br>" \
               "You will find a confirmation in your email."
    else:
        return "You need to <a href='/login'>login</a> before you confirm an order."

@route('/images/<filename:re:.*\.jpg>')
def image(filename):
    return static_file(filename, root='./images', mimetype='image/jpg')

@route('/css/<filename:re:.*\.css>')
def css(filename):
       return static_file(filename, root='./css')


if os.environ.get('Heroku'):
    run(host='0.0.0.0', port=os.environ.get('PORT'))
else:
    run(host='localhost', port=8080)