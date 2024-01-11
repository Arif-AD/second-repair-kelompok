from app import app
from app.controller import UserController
from flask import request, render_template, session

@app.route('/')
@app.route('/index')
def index():
    return render_template('landingpage.html')

@app.route('/home')
def home():
    user_name = session.get('name')
    return render_template('home.html', user_name=user_name)

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        return UserController.store()

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)

@app.route('/login', methods=['GET'])
def tampilkan_login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    return UserController.login()