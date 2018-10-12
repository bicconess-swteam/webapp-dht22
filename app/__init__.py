# app/__init__.py

import time, datetime

# third-party imports
from flask import Flask
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config

# db variable initialization
db = SQLAlchemy()

#local imports (I need to import there, here, after I initialize the db variable
from models import Information

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)
    
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route("/temp_now")
    def temp_now():
        import sys
        import Adafruit_DHT
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 2)
        if humidity is not None and temperature is not None:
            return render_template("temp_now.html",temp=temperature,hum=humidity).encode("utf-8")
        else:
            return render_template("problems_sorry.html")

    @app.route("/temp_historic", methods=['GET', 'POST'])
    def temp_historic():
        if request.method == 'GET':
            return render_template("temp_historic.html")

        from_date_str     = request.form.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
        to_date_str       = request.form.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
        
        app.logger.debug("From Date -> %s", from_date_str)
        app.logger.debug("To Date -> %s", to_date_str)

        info_temp_hum = Information.query.filter(Information.date.between(from_date_str,to_date_str)).all() 
        app.logger.debug("Info -> %s", info_temp_hum)
        return render_template("temp_historic.html", info            = info_temp_hum,
                                                     from_date       = from_date_str, 
                                                     to_date         = to_date_str)
    
    return app
