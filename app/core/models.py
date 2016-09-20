# Copyright 2014 SolidBuilds.com. All rights reserved
#
# Authors: Ling Thio <ling.thio@gmail.com>

from flask_user import UserMixin
from flask_user.forms import RegisterForm
from flask_wtf import Form
from wtforms import StringField, SubmitField, validators
from app import db
from datetime import datetime

# Define the User data model. Make sure to add the flask_user.UserMixin !!
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)

    # User authentication information (required for Flask-User)
    email = db.Column(db.Unicode(255), nullable=False, server_default=u'', unique=True)
    confirmed_at = db.Column(db.DateTime())
    password = db.Column(db.String(255), nullable=False, server_default='')
    reset_password_token = db.Column(db.String(100), nullable=False, server_default='')
    active = db.Column(db.Boolean(), nullable=False, server_default='0')

    # User information
    active = db.Column('is_active', db.Boolean(), nullable=False, server_default='0')
    first_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    last_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    company_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    priority = db.Column(db.Integer, nullable=False, server_default='1')

    # Relationships
    roles = db.relationship('Role', secondary='users_roles',
                            backref=db.backref('users', lazy='dynamic'))


# Define the Role data model
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), nullable=False, server_default=u'', unique=True)  # for @roles_accepted()
    label = db.Column(db.Unicode(255), server_default=u'')  # for display purposes


# Define the UserRoles association model
class UsersRoles(db.Model):
    __tablename__ = 'users_roles'
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))


# Define the User registration form
# It augments the Flask-User RegisterForm with additional fields
class MyRegisterForm(RegisterForm):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    company_name = StringField('Company name', validators=[
        validators.DataRequired('Company name is required')])


# Define the User profile form
class UserProfileForm(Form):
    first_name = StringField('First name', validators=[
        validators.DataRequired('First name is required')])
    last_name = StringField('Last name', validators=[
        validators.DataRequired('Last name is required')])
    company_name = StringField('Company name', validators=[
        validators.DataRequired('Company name is required')])
    submit = SubmitField('Save')


# Define the Product data model. 
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)

    # Product information
    
    product_name = db.Column(db.Unicode(50), nullable=False, server_default=u'')
    description = db.Column(db.Unicode(500), nullable=True, server_default=u'')
   

# Define the Feature Request data model.
class FeatureRequest(db.Model):
    __tablename__ = 'feature_requests'
    id = db.Column(db.Integer, primary_key=True)

    # Freature request information
    
    title = db.Column(db.Unicode(255), nullable=False, server_default=u'')
    description = db.Column(db.Unicode(500), nullable=False, server_default=u'')
    target_date = db.Column(db.DateTime, nullable=False, server_default=str(datetime.utcnow))
    client_priority = db.Column(db.Integer, nullable=False, server_default='1')
    global_priority = db.Column(db.Integer, nullable=False, server_default='1')
    ticket_url = db.Column(db.Unicode(500), nullable=True, server_default=u'')

    #Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
