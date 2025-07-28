from flask import Flask , flash , redirect , url_for
from config import *
from flask_wtf.csrf import CSRFProtect
from extentions import *
from flask_login import LoginManager
from blueprints.general import app as general
from blueprints.user import app as user
from blueprints.admin import app as admin 

from models.user import User

import random
import os


app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(admin)



app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)

app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    flash('وارد حساب کاربریتان شوید')
    return redirect(url_for('user.login'))



with app.app_context():
    db.create_all()



if __name__ == '__main__':
    app.run(debug=True , use_reloader = False)
