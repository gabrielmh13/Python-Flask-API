from app import db, ma

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

class UsersSchema(ma.Schema):
    class Meta:
        fields = ['id', 'username', 'password', 'name', 'email']

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)