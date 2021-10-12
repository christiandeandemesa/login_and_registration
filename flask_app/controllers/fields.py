from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.field import Field
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def main_page():
    return render_template('login.html')

@app.route('/dashboard')
def other_page():
    if 'field_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['field_id']
    }
    return render_template('logout.html', field = Field.read_by_id(data))

@app.route('/register', methods = ['post'])
def register():
    if not Field.valid_register(request.form):
        return redirect('/')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password']),
        'password_confirm': request.form['password_confirm']
    }
    id = Field.create(data)
    session['field_id'] = id
    return redirect('/dashboard')

@app.route('/login', methods = ['post'])
def login():
    field = Field.read_by_email(request.form)
    if not Field.valid_login(field, request.form['password']):
        return redirect('/')
    session['field_id'] = field.id
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')