from flask_wtf import FlaskForm
from wtforms import (StringField, TextAreaField, IntegerField, BooleanField,
                     RadioField)
from wtforms.validators import InputRequired, Length


# Book_review
# TODO: Change the rating system to a 5-star selector (use feathers as indicatives)
# Add a sub-list of quotes of the book to be displayed
class BookReview(FlaskForm):
    title = StringField('Book Title', validators=[InputRequired(),
                                             Length(min=4, max=100)])
    author= StringField('Author', validators=[InputRequired(),
                                             Length(min=4, max=100)])
    review_body = TextAreaField('Book review body',
                                validators=[InputRequired(),
                                            Length(max=200)])
    rating = IntegerField('Rating', validators=[InputRequired()])
    quotes = TextAreaField('Inspiring quotes',
                                validators=[InputRequired(),
                                            Length(max=200)])
    finished = BooleanField('Available', default='checked')