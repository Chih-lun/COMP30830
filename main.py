from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import requests
from statsmodels.tsa.api import VAR
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:group888@database-1.c5ekejexdq4k.us-east-1.rds.amazonaws.com/dublin_bike'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class bike_availibility(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Number = db.Column(db.Integer, nullable=False)
    Time = db.Column(db.DateTime)
    Available_bike_stands = db.Column(db.Integer)
    Available_bikes = db.Column(db.Integer)
    Status = db.Column(db.String(45))

    def __init__(self, ID, Number, Time, Available_bike_stands, Available_bikes, Status):
        self.ID = ID
        self.Number = Number
        self.Time = Time
        self.Available_bike_stands = Available_bike_stands
        self.Available_bikes = Available_bikes
        self.Status = Status

class weather(db.Model):
    ID = db.Column(db.Integer, primary_key=True, nullable=False)
    Time = db.Column(db.DateTime)
    Weather = db.Column(db.String(45))
    Temp = db.Column(db.Float)
    Feels_like = db.Column(db.String(45))
    Humidity = db.Column(db.Integer)

    def __init__(self, ID, Time, Weather, Temp, Feels_like, Humidity):
        self.ID = ID
        self.Time = Time
        self.Weather = Weather
        self.Temp = Temp
        self.Feels_like = Feels_like
        self.Humidity = Humidity

#build model
all_bike = bike_availibility.query.all()
bike_id = []
bike_number = []
bike_time = []
bike_available_bike_stands = []
bike_available_bikes = []
bike_status = []
for i in all_bike:
    bike_id.append(i.ID)
    bike_number.append(i.Number)
    bike_time.append(i.Time)
    bike_available_bike_stands.append(i.Available_bike_stands)
    bike_available_bikes.append(i.Available_bikes)
    bike_status.append(i.Status)
df_bike = pd.DataFrame(list(zip(bike_id, bike_number, bike_time, bike_available_bike_stands, bike_available_bikes, bike_status)),
                           columns =['ID', 'Number', 'Time', 'Available_bike_stands', 'Available_bikes', 'Status'])

all_weather = weather.query.all()
weather_id = []
weather_time = []
weather_weather = []
weather_temp = []
weather_feels_like = []
weather_humidity = []
for i in all_weather:
    weather_id.append(i.ID)
    weather_time.append(i.Time)
    weather_weather.append(i.Weather)
    weather_temp.append(i.Temp)
    weather_feels_like.append(i.Feels_like)
    weather_humidity.append(i.Humidity)
df_weather = pd.DataFrame(list(zip(weather_id, weather_time, weather_weather, weather_temp, weather_feels_like, weather_humidity)),
                              columns =['ID', 'Time', 'Weather', 'Temp', 'Feels_like', 'Humidity'])

df_combine = df_bike.merge(df_weather,left_on='Time', right_on='Time')

def build_model(number,step,type):
    # 10 min per step
    df_test_station=df_combine.groupby("Number").get_group(number)
    df_test_station = df_test_station.drop(['Number', 'ID_x', 'ID_y', 'Status', 'Weather', "Feels_like"], axis=1)
    df_test_station = df_test_station.set_index('Time')

    model = VAR(df_test_station)
    result = model.fit(4)
    pred = result.forecast(y=df_test_station.values, steps=step)
    df_pred = pd.DataFrame(pred, columns=["Available_bike_stands", "Available_bike", "Temp", "Humidity"])
    return int(round(df_pred[type].mean()))

@app.route('/')
def home():
    stations_data = requests.get('https://dublinbikeapi.herokuapp.com/stations')
    bike_availability_data = requests.get('https://dublinbikeapi.herokuapp.com/bike_availibility')
    weather_data = requests.get('https://dublinbikeapi.herokuapp.com/weather')

    predict_data = []
    for i in stations_data.json():
        prediction = {}
        prediction['Number'] = i['Number']
        prediction['Temp'] = round(build_model(i['Number'], 1, 'Temp'))
        prediction['Humidity'] = round(build_model(i['Number'], 1, 'Humidity'))
        prediction['Available_bike'] = round(build_model(i['Number'], 1, 'Available_bike'))
        prediction['Available_bike_stands'] = round(build_model(i['Number'], 1, 'Available_bike_stands'))
        predict_data.append(prediction)
    print(str(predict_data))

    return render_template('index.html', stations=stations_data.text, bike_availability=bike_availability_data.text, weather=weather_data.text, predict_data=str(predict_data))

if __name__ == '__main__':
    app.run(debug=True)