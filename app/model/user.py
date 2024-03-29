from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Users(db.Model):
    id = db.Column(db.BigInteger, primary_key = True, autoincrement = True)
    name = db.Column(db.String(230), nullable=False)
    email = db.Column(db.String(120), index = True, unique = True, nullable = False)
    password = db.Column(db.String(128), nullable = False)
    crateed_at = db.Column(db.DateTime, default = datetime.utcnow)
    updated_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    
    def setPassword(self, password):
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def checkPassword(self, password):
        result = check_password_hash(self.password, password)
        print(f"Password Match: {result}")
        return result