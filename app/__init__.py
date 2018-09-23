# app/__init__.py

# third-party imports
from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config
# from models import Information

# db variable initialization
db = SQLAlchemy()

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

    @app.route("/temp_historic", methods=['GET'])
    def temp_historic():
        from_date_str     = request.args.get('from',time.strftime("%Y-%m-%d 00:00")) #Get the from date value from the URL
        to_date_str       = request.args.get('to',time.strftime("%Y-%m-%d %H:%M"))   #Get the to date value from the URL
        range_h_form      = request.args.get('range_h','');  #This will return a string, if field range_h exists in the request
        range_h_int       = "nan"  #initialise this variable with not a number
        
        
        # temperatures, humidities, timezone, from_date_str, to_date_str = 
        # Create new record tables so that datetimes are adjusted back to the user browser's time zone.
        # time_adjusted_temperatures = []
        # time_adjusted_humidities   = []
        # for record in temperatures:
          #  local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
           # time_adjusted_temperatures.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])

        # for record in humidities:
          #  local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
          #  time_adjusted_humidities.append([local_timedate.format('YYYY-MM-DD HH:mm'), round(record[2],2)])

        # print "rendering lab_env_db.html with: %s, %s, %s" % (timezone, from_date_str, to_date_str)

        # return render_template("lab_env_db.html", timezone        = timezone,
          #                                        temp            = time_adjusted_temperatures,
           #                                       hum             = time_adjusted_humidities, 
            #                                      from_date       = from_date_str, 
             #                                     to_date         = to_date_str,
              #                                    temp_items      = len(temperatures),
               #                                   query_string    = request.query_string,
                #                                  hum_items       = len(humidities))

    return app
