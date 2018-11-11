# app/__init__.py
# coding: utf-8

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

    @app.route("/last_temp")
    def last_temp():
        import pygal
        import sys
        reload(sys)
        sys.setdefaultencoding("utf-8")
        information = Information.query.order_by(Information.id.desc()).first()
        gauge = pygal.SolidGauge(half_pie=True, inner_radius=0.40,style=pygal.style.LightColorizedStyle(value_font_size=10), show_legend=False)
        symbol_degree = ("º".encode('utf-8'))
        percent_formatter = lambda x: '{:.10g}%'.format(x)
        celsius_formatter = lambda x: '{:.10g}{simbol}C'.format(x, simbol=symbol_degree)
        gauge.add('Temperatura', [{'value': information.temperature, 'max_value': 50}], formatter=celsius_formatter)
        gauge.add('Humedad', [{'value': information.humidity, 'max_value': 100}], formatter=percent_formatter)
        gauge_data = gauge.render_data_uri()
        return render_template("temp_now.html",temp=information.temperature,hum=information.humidity,gauge_data=gauge_data)

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

    @app.route("/temp_graphic", methods=["GET", "POST"])
    def temp_graphics():
        import pygal
        if request.method == "GET":
            graph = pygal.Line()
            graph.add('line', []) 
            graph_data = graph.render_data_uri()
            return render_template("temp_graphics.html", graph_data = graph_data)

        from_date_str = request.form.get('from',time.strftime("%Y-%m-%d 00:00"))
        to_date_str   = request.form.get('to',time.strftime("%Y-%m-%d 23:59"))  
        informations = db.session.query(Information).filter(Information.date >= from_date_str, Information.date <= to_date_str).all()
        dates_str = []
        temperatures_str = []
        humidities_str = []

        app.logger.debug("Informations -> %s", informations)

        for info in informations:
            dates_str.append(info.date.strftime('%Y-%m-%d %H:%M:%S'))
            temperatures_str.append(float(info.temperature))
            humidities_str.append(float(info.humidity))
       
        app.logger.debug("Temperatures -> %s", temperatures_str)
        app.logger.debug("Humidities -> %s", humidities_str)
        app.logger.debug("Dates -> %s", dates_str)       
        app.logger.debug("Len Dates -> %s", len(dates_str))

        dates_str_major = []
        count = 0        
        while count < len(dates_str):
             app.logger.debug("Dates_str -> %s", count)
             dates_str_major.append(dates_str[count])
             count += len(dates_str)/10
        
        style_graph_temp = pygal.style.CleanStyle(value_font_size=10)
        style_graph_hum  = pygal.style.CleanStyle(value_font_size=10)
        style_graph_temp.background = '#fff1e7'
        style_graph_hum.background = '#fff1e7'
        style_graph_temp.colors = ('#91a8d0', '#91a8d0')
        style_graph_hum.colors = ('#88B04B', '#88B04B')

        graph_temperatures = pygal.Line(x_label_rotation=20, x_labels_major_every=len(dates_str)/10, show_minor_x_labels=False, style=style_graph_temp, show_legend=False)
        graph_temperatures.title = 'Graphics of Temperatures'
        graph_temperatures.x_labels = dates_str 
        graph_temperatures.x_labels_major = [dates_str_major]
        graph_temperatures.add("Temperature", temperatures_str, dots_size=0.09)
        graph_data_temp = graph_temperatures.render_data_uri()

        graph_humidities = pygal.Line(x_label_rotation=20, x_labels_major_every=len(dates_str)/10, show_minor_x_labels=False, style=style_graph_hum, show_legend=False)
        graph_humidities.title = 'Graphics of Humidities'
        graph_humidities.x_labels = dates_str
        graph_humidities.x_labels_major = [dates_str_major]
        graph_humidities.add("Humidity", humidities_str, dots_size=0.09)
        graph_data_hum = graph_humidities.render_data_uri()

        return render_template("temp_graphics.html", graph_data_temp = graph_data_temp, graph_data_hum = graph_data_hum, from_date=from_date_str, to_date=to_date_str)

    return app
