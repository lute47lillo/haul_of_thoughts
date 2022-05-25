import os
import psycopg2
from flask import Flask, render_template, request, jsonify, url_for, flash, redirect
from review_data import BookReview


#ACTIVATE BELOW FOR REC SYSTEM Create functions for requesting the data needed
#from recommendation_model import get_predictions

# Get connection to the PostgreSQL DB
def connect_db():
    con = psycopg2.connect(host='localhost',
                            database='book_db',
                            user=os.environ['DB_USERNAME'],
                            password=os.environ['DB_PASSWORD'])
    return con

app = Flask(__name__)
#The flash() function stores flashed messages in the client’s browser session, which requires setting a secret key. 
app.config['SECRET_KEY'] = '54e24481c2936c021ab570ea568d81db3f7d12da6fe3cdda'

# WTF forms for book review
book_reviews = [{
    'title': 'La tabla de Flandes',
    'author': 'Arturo Pérez-Reverte',
    'review_body': 'Great book!',
    'rating': 4,
    'available': True,
    'quotes': 'Dios mueve al jugador y este a la pieza. ¿Qué Dios detrás de Dios la trama empieza de polvo y sueño y agonías...?'},
    ]

# Page to render the base.html file from template dir HOMEPAGE
@app.get("/")
def index_get():
    return render_template("index.html")

@app.route('/home/')
def home():
    return render_template('index.html')

#book_review = book_reviews for old connection
@app.route('/book_thought/')
def book_thought():
    # Set-UP connections
    conect = connect_db()
    cursor = conect.cursor()
    
    # Execute commands to retrieve
    cursor.execute('SELECT * FROM books;')
    books = cursor.fetchall()
    
    # Disconect
    cursor.close()
    conect.close()
    
    return render_template('book_thought.html', books=books)

@app.route('/book_recommendation/')
def book_recommendation():
    return render_template('book_rec.html')

# Create a new book review
@app.route('/review/', methods=('GET', 'POST'))
def review():
    review_sheet = BookReview()
    
    # Check if error, else validate and submit new review
    if review_sheet.validate_on_submit():
        book_reviews.append({'title': form.title.data,
                             'body_review': form.description.data,
                             'author': form.title.data,
                             'rating': form.price.data,
                             'quotes': form.title.data,
                             'finsihed': form.available.data
                             })
        return redirect(url_for('book_thought'))
        
    return render_template('book_review.html')


if __name__ == "__main__":
    app.run(debug=True)
    
