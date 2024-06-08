import datetime

import jwt

SECRET_KEY = 'I8qT7L9q2Vw8F8p9V9R8X2K1K0Q2X0X4R3H2T7L8'
headers = {
    "alg": "HS256",
    "typ": "JWT"
}
ALGORITHM = 'HS256'


def get_jwt_token(load: object, expiration_minutes: int = 30):
    return jwt.encode({
        'load': load,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    }, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, verify=True, algorithms=[ALGORITHM])
