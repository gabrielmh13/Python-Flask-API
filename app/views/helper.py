from app import db, key
from ..models.refreshToken import RefreshToken, refreshToken_schema
import datetime
import time
import jwt

def removeRefreshToken(userId):
    refreshToken = RefreshToken.query.filter(RefreshToken.userId == userId).first()

    if refreshToken:
        db.session.delete(refreshToken)
        db.session.commit()

def generateRefreshToken(userId):
    removeRefreshToken(userId)

    expiresIn = time.mktime((datetime.datetime.now() + datetime.timedelta(seconds=30)).timetuple())
    refreshToken = RefreshToken(expiresIn, userId)
    result = refreshToken_schema.dump(refreshToken)

    try:
        db.session.add(refreshToken)
        db.session.commit()

        return result
    except:
        return None

def generateAccessToken(userId):
    return jwt.encode({'sub': userId, 'exp':  time.mktime((datetime.datetime.now() + datetime.timedelta(seconds=10)).timetuple())}, key, algorithm="HS256")