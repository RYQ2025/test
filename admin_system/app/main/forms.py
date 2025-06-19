from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class DataSubmissionForm(FlaskForm):
    data_content = TextAreaField('Data Content', validators=[DataRequired()], render_kw={'rows': 10, 'cols': 50})
    submit = SubmitField('Submit Data')
