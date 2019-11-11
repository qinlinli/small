from datetime import datetime

from werkzeug.security import generate_password_hash

from miniapp.corelibs.stone import db
from models.base import Base


class User(Base):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(255), nullable=False)
    sex = db.Column(db.Integer, nullable=False)
    mobile = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    identity_id = db.Column(db.String(32), nullable=True)
    created = db.Column(db.DateTime, default=datetime.now)
    updated = db.Column(db.DateTime, default=datetime.now,
                        onupdate=datetime.now)
    deleted = db.Column(db.Boolean, default=False)

    @classmethod
    def get_by_mobile(cls, mobile):
        return cls.query.filter(cls.mobile == mobile).first()

    @classmethod
    def create(cls, data):
        password = generate_password_hash(data.get('password'))
        data.update({'password':password})
        obj = cls(**data)
        obj.save()
        return object

