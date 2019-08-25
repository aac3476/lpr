# -*- coding: utf-8 -*-  
"""
Create on 07-22 21:08 2019
@Author ywx 
@File forms.py
"""


from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField,DateTimeField,SelectField
from wtforms.validators import DataRequired,Email

class LoginForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    passw = StringField('passw',validators=[DataRequired()])


