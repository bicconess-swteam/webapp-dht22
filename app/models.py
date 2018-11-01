# app/models.py

from app import db

class Information(db.Model):

    """
    Create an Information table
    """
    
    __tablename__ = 'InformationTempHum'
   
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    temperature = db.Column(db.Integer)
    humidity = db.Column(db.Integer)    

