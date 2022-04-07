import requests
import datetime
import pymysql

class Station():
    def __init__(self, time, number, address, latitude, longitude, available_bike_stands, available_bikes, status):
        self.time = time
        self.number = number
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.available_bike_stands = available_bike_stands
        self.available_bikes = available_bikes
        self.status = status

class Weather():
    def __init__(self, time, weather, temp, feels_like, humidity):
        self.time = time
        self.weather = weather
        self.temp = temp
        self.feels_like = feels_like
        self.humidity = humidity

now = datetime.datetime.now()
bike_stations = []

BIKE_API = "12b14fd3d4ed7ad3c69cd088c54135d43d4e61c5"
BIKE_URL = "https://api.jcdecaux.com/vls/v1/stations"
bike_request = requests.get(BIKE_URL, params={"apiKey": BIKE_API, "contract": 'Dublin'})
bike_data = bike_request.json()

for i in bike_data:
    number = i['number']
    address = i['address']
    latitude = i['position']['lat']
    longitude = i['position']['lng']
    available_bike_stands = i['available_bike_stands']
    available_bikes = i['available_bikes']
    status = i['status']
    bike_stations.append(Station(now, number, address, latitude, longitude, available_bike_stands, available_bikes, status))

WEATHER_API = '1a1828cc886b56d6b2bf7f37dc0a4b14'
WEATHER_URL = 'https://api.openweathermap.org/data/2.5/weather?q=Dublin'
weather_request = requests.get(WEATHER_URL, params={'appid': WEATHER_API, 'units':'metric'})
weather_data = weather_request.json()
weather = Weather(now, weather_data['weather'][0]['main'], weather_data['main']['temp'], weather_data['main']['feels_like'], weather_data['main']['humidity'])

connection = pymysql.connect(host='database-1.c5ekejexdq4k.us-east-1.rds.amazonaws.com', user='admin', password='group888', database='dublin_bike')

with connection:
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM stations')
        rows = cursor.fetchall()
        current_stations_number = [i[0] for i in rows]

connection = pymysql.connect(host='database-1.c5ekejexdq4k.us-east-1.rds.amazonaws.com', user='admin', password='group888', database='dublin_bike')

with connection:
    with connection.cursor() as cursor:
        # bike information
        for i in bike_stations:
            # add new station if any is new
            if i.number not in current_stations_number:
                sql = "INSERT INTO `stations` (`Number`, `Address`, `Latitude`, `Longitude`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (i.number, i.address, i.latitude, i.longitude))
                connection.commit()
                print('New station added')

            # insert new bike availibility data
            sql = "INSERT INTO `bike_availibility` (`Number`, `Time`, `Available_bike_stands`, `Available_bikes`, `Status`) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (i.number, i.time, i.available_bike_stands, i.available_bikes, i.status))
            connection.commit()
            print("New bike info added")

        # weather information
        sql = "INSERT INTO `weather` (`Time`, `Weather`, `Temp`, `Feels_like`, `Humidity`) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (weather.time, weather.weather, weather.temp, weather.feels_like, weather.humidity))
        connection.commit()
        print("New weather info added")

print(now)