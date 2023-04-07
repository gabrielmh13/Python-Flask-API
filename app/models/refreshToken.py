from app import db, ma
import uuid

class RefreshToken(db.Model):
    __tablename__ = 'refresh_token'

    id = db.Column(db.String, unique=True, nullable=False, primary_key=True)
    expiresIn = db.Column(db.Integer, nullable=False)
    userId = db.Column(db.Integer, nullable=False)

    def __init__(self, expiresIn, userId):
        self.id = uuid.uuid4()
        self.expiresIn = expiresIn
        self.userId = userId

class RefreshTokenSchema(ma.Schema):
    class Meta:
        fields = ['id', 'expiresIn', 'userId']

refreshToken_schema = RefreshTokenSchema()