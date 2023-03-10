import os 
import uuid
from flask import Flask, render_template, request, redirect, jsonify
from flask.helpers import make_response, url_for 
from flask_mail import Mail, Message 
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
app.config["UPLOAD_FOLDER"] = "static\\UploadedFiles"
app.config["MONGO_URI"] = "mongodb://localhost:27017"
client = MongoClient('localhost', 27017)
db = client['FlaskWebDB']
mail = Mail(app)


app.config['MAIL_SERVER']='smtp.yandex.com.tr'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'HTTP.403@yandex.com'
app.config['MAIL_PASSWORD'] = 'Retropy18%'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


mail.init_app(app)


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
            activisionuid = uuid.uuid4()
            db.users.insert_one({"name": name, "birthdate": birthdate, "gender": gender, "email": email, "password": password, "code": activisionuid.__str__(), "isTrue": False})
            url = "/mailS/" + email + "/"+ activisionuid.__str__()
            return redirect(url)
       else:
            return '<script>alert("fuck off")</script>'
   

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = request.form
        email = result.get("email")
        password = result.get("pass")
        control = db.users.find_one({"email": email, "password": password})
        if control != None and control["isTrue"]:
            resp = make_response(render_template('profile.html', result=control, info = "JPG or PNG no larger than 5 MB"))
            resp.set_cookie('userID', email)
            return resp 
            return render_template('profile.html', result=control, info = "JPG or PNG no larger than 5 MB")
        else:
            return '<script>alert("fuck off")</script>'
    return render_template('login.html')


@app.route('/update_profile', methods = ['POST'])
def update_profile():
    if request.method == 'POST':
        result = request.form
        email = result.get('email')
        gender = result.get('gender')
        username = result.get('username')
        dbresult = db.users.update_one({"email": email},{"$set": {"username": username, "gender": gender}})
        personresult = db.users.find_one({"email": email})
        return render_template('profile.html', result=personresult)

@app.route("/upload", methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        split_tup = os.path.splitext(file.filename)
        extension = split_tup[1]
        photouid = uuid.uuid4() 
        photouid = str(photouid) + extension
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], photouid))
        user = request.cookies.get('userID')
        personalresult = db.users.find_one({"email": user })
        photo = db.users.update_one({"email": user}, {"$set":{"photoName": photouid}})
        return render_template('profile.html', result= personalresult, info = "Profile foto eklendi")

###Mail###

@app.route("/mailS/<email>/<code>")
def mailSenderr(email, code):
    msg = Message("Hitler Was Right",
    sender="HTTP.403@yandex.com",
    recipients=[email]
)
    msg.body = f"Clik it DUMASS http://127.0.0.1:5000/mailS/" + code
    mail.send(msg)
    return "Mesaj gönderildi"



@app.route("/code_check/<email>/<code>")
def codeChecker(email,code):
    code = db.users.update_one({"code": code}, {"$set":{"isTrue": True}})
    return redirect("/login")

if "__main__" == __name__:
    app.run(host= "0.0.0.0")