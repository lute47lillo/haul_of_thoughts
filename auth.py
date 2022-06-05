from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

import os
import psycopg2

auth = Blueprint('auth', __name__)


# Get connection to the PostgreSQL DB
os.environ['DB_USERNAME'] = 'admin'
os.environ['DB_PASSWORD'] = 'PurplePine015'
def connect_db():
    con = psycopg2.connect(host='localhost',
                            database='book_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return con

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        user_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # TODO: GO Through all the emails on user table and check that the email does not exist
        """
            CURRENT ERROR if EMAIL is Duplicated
            psycopg2.errors.UniqueViolation: duplicate key value violates unique constraint "users_email_key"
            DETAIL:  Key (email)=(lillo@gmail.com) already exists.
        """
        user = False
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(user_name) < 2:
            flash('User name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            
            conection = connect_db()
            cursor = conection.cursor()
            cursor.execute('INSERT INTO users (email, password, user_name)'
                    'VALUES (%s, %s, %s)',
                    (email, password1, user_name))
            conection.commit()
            cursor.close()
            conection.close()
            
            
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)