from statsmodels.tsa.api import VAR
from sqlalchemy import create_engine
import pandas as pd

URI = "database-1.c5ekejexdq4k.us-east-1.rds.amazonaws.com"
PORT = "3306"
DB = "dublin_bike"
USER = "admin"
PASSWARD = "group888"

engine = create_engine("mysql+mysqlconnector://{}:{}@{}:{}/{}".format(USER, PASSWARD, URI, PORT, DB))
df_bike = pd.read_sql_table("bike_availibility", engine, parse_dates="True", index_col=0)
df_weather = pd.read_sql_table("weather", engine, parse_dates="True", index_col=0)

df_combine = df_bike.merge(df_weather,left_on='Time', right_on='Time')

def build_model(number,step):
    # 10 min per step
    df_test_station=df_combine.groupby("Number").get_group(number)
    df_test_station = df_test_station.drop(['Number', 'ID_x', 'ID_y', 'Status', 'Weather', "Feels_like"], axis=1)
    df_test_station = df_test_station.set_index('Time')
    
    model = VAR(df_test_station)
    result = model.fit(4)
    pred = result.forecast(y=df_test_station.values, steps=step)
    df_pred = pd.DataFrame(pred, columns=["Aviable_bike_stands", "Available_bike", "Temp", "Humidity"])
    return df_pred


# print(build_model(10, 2)["Temp"]) simple test