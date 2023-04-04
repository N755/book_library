from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class BookForm(Form):
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    publisher = StringField('Publisher', validators=[DataRequired()])
    year = IntegerField('Year', validators=[DataRequired(), NumberRange(min=1)])
    pages = IntegerField('Pages', validators=[DataRequired(), NumberRange(min=1)])

