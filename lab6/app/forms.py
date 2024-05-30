from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange

class ReviewForm(FlaskForm):
    rating = IntegerField('Оценка', validators=[DataRequired(), NumberRange(min=0, max=5)])
    text = TextAreaField('Текст отзыва', validators=[DataRequired()])
    submit = SubmitField('Добавить отзыв')
