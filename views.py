"""
    Author: Lute Lillo Portero
    lute47lillo
"""
import os
import psycopg2
from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from flask import Blueprint

# Create a blueprint of init app (Easier way to divide the project)
views = Blueprint('views', __name__)

# Set variable environment for the database
# TODO: Make them private
os.environ['DB_USERNAME'] = 'admin'
os.environ['DB_PASSWORD'] = 'PurplePine015'

#ACTIVATE BELOW FOR REC SYSTEM Create functions for requesting the data needed
#from recommendation_model import get_predictions

# Get connection to the PostgreSQL DB
def connect_db():
    con = psycopg2.connect(host='localhost',
                            database='book_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return con


# Page to render the base.html file from template dir HOMEPAGE
@views.get("/")
def index_get():
    return render_template("index.html")

@views.route('/')
def home():
    return render_template('index.html')

'''
    1. Call DB connection and fetch all data into the web browser
    2. If remove is called, delete the entry for which id is matched
'''
@views.route('/book_thought/',methods=('GET', 'POST'))
def book_thought():
    
    # Set-UP connections
    conect = connect_db()
    cursor = conect.cursor()
    
    if 'remove' in request.form:
        book_id = int(request.form['index'])
        print(book_id)
      
        cursor.execute("DELETE FROM books WHERE book_id='%s'"  % book_id)
        conect.commit()
        cursor.close()
        conect.close()
        return redirect(url_for('views.book_thought'))
    
    # Execute commands to retrieve
    cursor.execute('SELECT * FROM books;')
    books = cursor.fetchall()
    
    # Disconect
    cursor.close()
    conect.close()
    
    return render_template('book_thought.html', books=books)


@views.route('/book_recommendation/')
def book_recommendation():
    return render_template('book_rec.html')

'''
    Create a new entry review/thought idea into the DB
    TODO: retrieve the user connected in that moment and save it to that user.
'''
@views.route('/review/', methods=('GET', 'POST'))
def review():
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        quotes = request.form['quotes']
        review = request.form['review']
        print(title)

        conection = connect_db()
        cursor = conection.cursor()
        cursor.execute('INSERT INTO books (title, author, quotes, review)'
                    'VALUES (%s, %s, %s, %s)',
                    (title, author, quotes, review))
        conection.commit()
        cursor.close()
        conection.close()
        return redirect(url_for('views.book_thought'))
        
    return render_template('book_review.html')

"""
    1. From book_thought.html we select X book to be edited, 
    then index is requested and form is loaded with previous
    data.
    2. Save changes button is pressed and changes are saved
    to the DB
    #TODO: When editing, the order of the databse changes showing the updated element last
    MAYBE UPDATE THE DATE ADDED TO BE UPDATEED

"""
last_access_id = []
@views.route('/edit/', methods=['GET', 'POST'])
def edit():

    if request.method == 'POST':
        
        # Load previous data of X book
        if 'index' in request.form:
            # do things
            book_id = int(request.form['index'])
            last_access_id.append(book_id)
        
            # Set-UP connections
            conect = connect_db()
            cursor = conect.cursor()
    
            # Execute commands to retrieve
            cursor.execute("SELECT * FROM books WHERE book_id='%s'"  % book_id)
            books = cursor.fetchall()

            # Disconect
            cursor.close()
            conect.close()
    
            return render_template('edit_thought.html', books=books)
        
        else:
            # Save changes button to load new data into the DB.
            title = request.form['title']
            author = request.form['author']
            quotes = request.form['quotes']
            review = request.form['review']
            print(title)

            conection = connect_db()
            cursor = conection.cursor()
            
            
            # Create SQL Query
            sql = """   UPDATE books
                        SET title = %s, author = %s, quotes= %s, review=%s
                        WHERE book_id = %s;
                  """
            # Since you cannot access the edit page unless you selected a book_id by editing
            # the last access will always be the one on edition.
            # TODO: Maybe when deleting -> Remember to delete the list
            cursor.execute(sql, (title, author, quotes, review, last_access_id[-1]))
                    
            conection.commit()
            cursor.close()
            conection.close()
            
            return redirect(url_for('views.book_thought'))
        
    return render_template('book_thought.html')

