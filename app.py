from flask import Flask, render_template, request, jsonify, url_for, flash, redirect


#from recommendation_model impor -> Create functions for requesting the data needed
#from recommendation_model import get_predictions

app = Flask(__name__)
#The flash() function stores flashed messages in the client’s browser session, which requires setting a secret key. 
app.config['SECRET_KEY'] = '54e24481c2936c021ab570ea568d81db3f7d12da6fe3cdda'


# TODO: Make list prettier, and empty (not showing) if list is actually empty
messages = [{'title': 'Book title',
             'content': 'Book review'},
            ]



# Page to render the base.html file from template dir HOMEPAGE
@app.get("/")
def index_get():
    return render_template("index.html")

@app.route('/home/')
def home():
    return render_template('index.html')

@app.route('/book_thought/')
def book_thought():
    return render_template('book_thought.html', messages=messages)

@app.route('/book_recommendation/')
def book_recommendation():
    return render_template('book_rec.html')

# Create a new book review
@app.route('/review/', methods=('GET', 'POST'))
def review():
    # Check that a POST request is sent
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        # Check for missing parts of the review
        if not title:
            flash('Book title is required!')
        elif not content:
            flash('Review body is required!')
        else:
            messages.append({'title': title, 'content': content})
            return redirect(url_for('book_thought'))
        
    return render_template('book_review.html')


if __name__ == "__main__":
    app.run(debug=True)
    
