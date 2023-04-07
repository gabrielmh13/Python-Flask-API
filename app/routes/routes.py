from app import app
from flask import jsonify, render_template
from ..views import users
from ..middlewares import ensureAuthentication

@app.route('/', methods=['GET'])
def root():
    return jsonify({'message': 'Hello World!'})

@app.route('/users', methods=['POST'])
def post_user():
    return users.post_user()

@app.route('/users', methods=['GET'])
@ensureAuthentication.verifyToken
def get_users():
    return users.get_users()

@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    return users.get_user(id)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    return users.update_user(id)

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    return users.delete_user(id)

@app.route('/login', methods=['POST'])
def auth_user():
    return users.auth_user()

@app.route('/refresh-token', methods=['POST'])
def refresh_token():
    return users.refresh_token()

@app.route('/users-template', methods=['GET'])
def get_usersTemplate():
    usersList = users.get_usersTemplate()
    return render_template('template.html', users=usersList)