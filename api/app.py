from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:group888@dublinbike.c5ekejexdq4k.us-east-1.rds.amazonaws.com/dublin_bike'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class stations(db.Model):
    Number = db.Column(db.Integer, primary_key=True, nullable=False)
    Address = db.Column(db.String(45))
    Latitude = db.Column(db.Float)
    Longitude = db.Column(db.Float)

    def __init__(self, Number, Address, Latitude, Longitude):
        self.Number = Number
        self.Address = Address
        self.Latitude = Latitude
        self.Longitude = Longitude


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

@app.route('/')
def index():
    return 'successful'

@app.route('/stations', methods=['GET'])
def get_stations():
    all_stations = stations.query.all()
    reply = []
    for i in range(len(all_stations)):
        station = {}
        station['Number'] = all_stations[i].Number
        station['Address'] = all_stations[i].Address
        station['Latitude'] = all_stations[i].Latitude
        station['Longitude'] = all_stations[i].Longitude
        reply.append(station)
    return jsonify(reply)

@app.route('/bike_availibility')
def get_bike_availibility():
    max_time = db.session.query(func.max(bike_availibility.Time)).first()
    all_bike_availibility = bike_availibility.query.filter(bike_availibility.Time == max_time[0]).order_by(bike_availibility.Number).all()
    print(all_bike_availibility)
    reply = []
    for i in range(len(all_bike_availibility)):
        bike = {}
        bike['ID'] = all_bike_availibility[i].ID
        bike['Number'] = all_bike_availibility[i].Number
        bike['Time'] = all_bike_availibility[i].Time
        bike['Available_bike_stands'] = all_bike_availibility[i].Available_bike_stands
        bike['Available_bikes'] = all_bike_availibility[i].Available_bikes
        bike['Status'] = all_bike_availibility[i].Status
        reply.append(bike)
    return jsonify(reply)

if __name__ == '__main__':
    app.run()