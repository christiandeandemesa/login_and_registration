from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Field:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.password_confirm = data['password_confirm']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create(cls, data):
        query = 'INSERT INTO fields (first_name, last_name, email, password, password_confirm) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, %(password_confirm)s);'
        result = connectToMySQL('registration').query_db(query, data)
        return result

    @classmethod
    def read_by_id(cls, data):
        query = 'SELECT * FROM fields where id = %(id)s;'
        result = connectToMySQL('registration').query_db(query, data)
        return cls(result[0])

    @classmethod
    def read_by_email(cls, data):
        query = 'SELECT * FROM fields WHERE email = %(email)s;'
        result = connectToMySQL('registration').query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @staticmethod
    def valid_register(field):
        is_valid = True
        query = 'SELECT * FROM fields WHERE email = %(email)s;'
        result = connectToMySQL('registration').query_db(query, field)
        if len(field['first_name']) < 1:
            flash('First name must be at least 1 character.', 'register')
            is_valid = False
        if len(field['last_name']) < 1:
            flash('Last name must be at least 1 character.', 'register')
            is_valid = False
        if len(result) >= 1:
            flash('Email is already taken.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(field['email']):
            flash('Invalid Email.', 'register')
            is_valid = False
        if len(field['password']) < 10:
            flash('Password must be at least 10 characters.', 'register')
            is_valid = False
        if field['password'] != field['password_confirm']:
            flash('Passwords do not match!', 'register')
        return is_valid

    @staticmethod
    def valid_login(field, password):
        if not field:
            flash('Invalid Login!', 'login')
            return False
        if not bcrypt.check_password_hash(field.password, password):
            flash('Invalid Login!', 'login') # Why won't wrong password show up?
            return False
        return True