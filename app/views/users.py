from app import db, key
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.users import Users, user_schema, users_schema
from ..models.refreshToken import RefreshToken
from .helper import generateAccessToken, generateRefreshToken, removeRefreshToken
import datetime

def post_user():
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']

    password_hash = generate_password_hash(password)

    user = Users(username, password_hash, name, email)

    try:
        db.session.add(user)
        db.session.commit()
        result = user_schema.dump(user)

        return jsonify(result), 201
    except:
        return jsonify({'message': 'Unable to create user'}), 500
    
def get_users():
    users = Users.query.all()

    if users:
        result = users_schema.dump(users)

        return jsonify(result)
    
    return jsonify({'message': 'Nothing found!'}), 404


def get_user(id):
    user = Users.query.get(id)

    if user:
        result = user_schema.dump(user)
        return jsonify(result)

    return jsonify({'message': 'User not found!'}), 404

def update_user(id):
    username = request.json['username']
    password = request.json['password']
    name = request.json['name']
    email = request.json['email']

    user = Users.query.get(id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404
    
    password_hash = generate_password_hash(password)

    try:
        user.username = username
        user.password = password_hash
        user.name = name
        user.email = email

        db.session.commit()

        result = user_schema.dump(user)
        return jsonify(result)
    
    except:
        return jsonify({'message': 'Unable to update user'}), 500
    
def delete_user(id):
    user = Users.query.get(id)

    if not user:
        return jsonify({'message': 'User not found!'}), 404
    
    try:
        db.session.delete(user)
        db.session.commit()

        return jsonify({'message': 'User deleted'})
    except:
        return jsonify({'message': 'Unable to delete user'}), 500
    
def auth_user():
    username = request.json['username']
    password = request.json['password']

    user = Users.query.filter(Users.username == username).first()

    if not user:
        return jsonify({'message': 'User or password are incorrect!'}), 401
    
    if check_password_hash(user.password, password):
        accessToken = generateAccessToken(user.id)
        refreshToken = generateRefreshToken(user.id)

        if not refreshToken:
            return jsonify({'message': 'Cannot create refresh token!'})

        return jsonify({'access_token': accessToken, 'refreshToken': refreshToken})
    
    return jsonify({'message': 'User or password are incorrect!'}), 401

def refresh_token():
    refreshToken = request.json['refreshToken']

    refreshToken = RefreshToken.query.filter(RefreshToken.id == refreshToken).first()

    if not refreshToken:
        return jsonify({'message': 'Invalid refresh token!'}), 401
    
    if(datetime.datetime.now() > datetime.datetime.fromtimestamp(refreshToken.expiresIn)):
        removeRefreshToken(refreshToken.userId)
        return jsonify({'message': 'Invalid refresh token!'}), 401
    
    accessToken = generateAccessToken(refreshToken.userId)

    return jsonify({'accessToken': accessToken})
    
def get_usersTemplate():
    users = Users.query.all()

    if users:
        return users
    
    return jsonify({'message': 'Nothing found!'}), 404