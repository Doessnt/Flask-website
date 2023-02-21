from flask import Flask, render_template, request

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
       return render_template('')

@app.route('/login')
def login():
   return render_template('login.html')

       







if "__main__" == __name__:
    app.run()