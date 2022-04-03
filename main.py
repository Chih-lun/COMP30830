from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def home():
    stations = requests.get('https://dublinbikeapi.herokuapp.com/stations').text
    bike_availability = requests.get('https://dublinbikeapi.herokuapp.com/bike_availibility').text
    return render_template('index.html', stations=stations, bike_availability=bike_availability)

if __name__ == '__main__':
    app.run(debug=True)