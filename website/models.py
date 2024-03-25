from email.policy import default
from pytz import timezone
from sqlalchemy import false
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    #model is a table 
    userid = db.Column(db.Integer, primary_key= True)
    email = db.Column(db.String(150), unique= True)
    username = db.Column(db.String(150), unique= True)
    password = db.Column(db.String(150))
    role = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(timezone=True), default= func.now())
    leaves = db.relationship('Leave', backref='user', passive_deletes=True)

    def get_id(self):
        return (self.userid)

class Leave(db.Model):
    leaveid = db.Column(db.Integer, primary_key= True)
    startdate = db.Column(db.String(50))
    enddate = db.Column(db.String(50))
    comment = db.Column(db.String(200))
    status = db.Column(db.Integer)
    leavedate_created = db.Column(db.DateTime(timezone=True), default= func.now())
    userid = db.Column(db.Integer, db.ForeignKey('user.userid', ondelete="CASCADE"), nullable = false)

    def get_id(self):
        return (self.leaveid)