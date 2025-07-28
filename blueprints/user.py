from flask import Blueprint , redirect , render_template, request , url_for , session , flash
from flask_login import login_user,login_required,current_user, logout_user
from extentions import db
from passlib.hash import sha256_crypt
from config import *

from models.user import *

app = Blueprint('user', __name__)




@app.route('/user/login' , methods = ['GET' , 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('user.dashboard'))

        return render_template("user/login.html")
    else:
        register = request.form.get('register', None)
        user_name = request.form.get('user_name', None)
        password = request.form.get('password', None)
        phone = request.form.get('phone', None)
     

        if register !=None:
            user = User.query.filter(User.user_name == user_name).first()
            if user != None:
                flash('نام کاربری دیگری انتخاب کنید')
                return redirect(url_for('user.login'))
            


            user = User(user_name= user_name , password = sha256_crypt.encrypt(password), phone = phone)
            db.session.add (user)
            db.session.commit()
            login_user(user)

            return redirect(url_for('user.dashboard'))
        
        else:
            user = User.query.filter(User.user_name == user_name).first()
            if user == None:
                flash('نام کاربری یا رمز اشتباه است')
                return redirect(url_for('user.login'))
            
            if sha256_crypt.verify(password , user.password):
                login_user(user)
                return redirect(url_for('user.dashboard'))
            else:
                flash('نام کاربری یا رمز اشتباه است')
                return redirect(url_for('user.login'))
        
        
    
@app.route('/user/dashboard', methods = ['GET' , 'POST'])
@login_required
def dashboard():
    if request.method == "GET":
        return render_template('user/dashboard.html')
    else:
        user_name = request.form.get('user_name', None)
        password = request.form.get('password', None)
        phone = request.form.get('phone', None)
        

        if current_user.user_name != user_name:
            user = User.query.filter(User.user_name == user_name).first()
            if user != None:
                flash('نام کاربری از قبل انتخاب شده است ')
                return redirect(url_for('user.login'))
            else:
                current_user.user_name = user_name
        if password != None:
            current_user.password = sha256_crypt.encrypt(password)

        current_user.phone = phone
       
        db.session.commit()

        return redirect(url_for('user.dashboard'))



@app.route('/user/logout', methods = ['GET'])
@login_required
def logout():
    logout_user()
    flash('با موفقیت خارج شدید')
    return redirect('/')
