from db_connect import db
from datetime import datetime

class Target(db.Model):
    __tablename__ = 'target'
    id = db.Column(db.Integer, primary_key=True,
                       nullable=False, autoincrement=True)
    fl_item = db.Column(db.String(256),nullable=False)
    fl_type = db.Column(db.String(256), nullable=False)

    def __init__(self, fl_item, fl_type):
        self.fl_item = fl_item
        self.fl_type = fl_type


class Flower(db.Model):
    __tablename__ = 'realtime_flower'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    poomname = db.Column(db.String(100), nullable=False)
    goodname = db.Column(db.String(100), nullable=False)
    lvname = db.Column(db.String(100), nullable=False)
    qty = db.Column(db.Integer(), nullable=False)
    cost = db.Column(db.Integer(), nullable=False)
    dateinfo = db.Column(db.String(100), nullable=False)

    def __init__(self, poomname, goodname, lvname, qty, cost, dateinfo):
        self.poomname = poomname
        self.email = goodname
        self.phone = lvname
        self.qty = qty
        self.cost = cost
        self.dateinfo = dateinfo


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    author = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    likeit = db.Column(db.Integer, default=0)
    imagename = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, author, content, imagename):
        self.author = author
        self.content = content
        self.imagename = imagename

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, nullable=False,
                   autoincrement=True)
    user_id = db.Column(db.String(100), nullable=False,
                        unique=True)
    user_pw = db.Column(db.String(100), nullable=False)

    def __init__(self, user_id, user_pw):
        self.user_id = user_id
        self.user_pw = user_pw