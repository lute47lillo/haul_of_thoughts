from flask import Flask, render_template, request, jsonify


#from recommendation_model impor -> Create functions for requesting the data needed
from recommendation_model import get_predictions

app = Flask(__name__)

# Page to render the base.html file from template dir HOMEPAGE
@app.get("/")
def index_get():
    return render_template("index.html")

@app.route('/home/')
def home():
    return render_template('index.html')

@app.route('/book_thought/')
def book_thought():
    return render_template('book_thought.html')

@app.route('/book_recommendation/')
def book_recommendation():
    return render_template('book_rec.html')


'''
@app.post("/predict")
def predict():
    text = request.get_json().get("message")   # ask for input user -> Based on what book
    # TODO: Check for valid text
    
    pred_books = get_predictions(text)           # Predict from rec_system
    message = {"answer": pred_books}
    return jsonify(message)

'''
if __name__ == "__main__":
    app.run(debug=True)
    
