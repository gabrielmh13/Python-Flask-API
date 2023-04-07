from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


app = Flask(__name__)
key = '40244393-20dc-477a-aef6-3a390cb1f4ea'

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/treinamento3'

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)

from .models import users, refreshToken
from .routes import routes