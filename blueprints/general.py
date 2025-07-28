from flask import Blueprint, render_template, request, session, flash, redirect,url_for
from flask_login import current_user
app = Blueprint('general', __name__)


@app.route('/')
def main():
    return render_template("main.html")

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/rules')
def rules():
    return render_template('rules.html')



@app.route('/comments')
def comments():
    return render_template('comments.html')