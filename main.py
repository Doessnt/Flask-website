from flask import Flask, render_template, request, redirect, jsonify
from flask.helpers import make_response, url_for 
from pymongo import MongoClient
app = Flask(__name__)
# Home sayfası
# Register sayfası
# Login Sayfası
# Cookie mantığı
# Giriş yapıldıktan sonra belirli bölgelerle kullanıcı ile ilgili bilgiler veritabanında  çekilip sayfada gösterilecek 
# Dosya yükleme ekranı olucak
# Dosya yüklenirken uzantı kontrolü yapılacak
# Yüklenen fotoğrafı yüklenen kişinin ekranında gözükücek

##############################################################################################################################
app.config["MONGO_URI"] = "mongodb://localhost:27017"
client = MongoClient('localhost', 27017)
db = client['FlaskWebDB']

@app.route('/home')
@app.route('/')
def homePage():
    return render_template('index.html')


@app.route('/register', methods = ['POST', 'GET'])
def registerPage():
   if request.method == 'GET':
       return render_template('register.html')
   elif request.method == 'POST':
       result = request.form
       name = result.get("name")
       birthdate = result.get("birthday")
       gender = result.get("gender")
       email = result.get("email")
       password = result.get("password")
       control = db.users.find_one({"email": email})
       if control == None:
            db.users.insert_one({"name": name, "birthdate": birthdate, "gender": gender, "email": email, "password": password})
            return redirect("login")
       else:
            return '<script>alert("fuck off")</script>'
   

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/cookieform')
def cookieForm():
    return render_template('cookiewriter.html')


@app.route('/setcookie', methods = ['POST'])
def setcookie():
    if request.method == 'POST':
        user = request.form['userId']
        resp = make_response(redirect('getcookie'))
        resp.set_cookie('userId',user)
        return resp
    
@app.route('/add')
def add():
    db.users.insert_one({"username": "admin", "password": "admin"})
    return jsonify(message = 'success')



@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userId')
    return '<h1> sizin cookiniz :' + name + '</h1>'




if "__main__" == __name__:
    app.run()