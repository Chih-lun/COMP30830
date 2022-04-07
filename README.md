# COMP30830 Software Engineering - Dublin Bikes (Group 8)

# Introduction
This is an web application which is developed in Python Flask Framework. It includes the information of all bike stations in Dublin, the weather, and the prediction.

# How this application works
There are 3 major parts in this application. First, it displays the locations of all stations. According to the station, it demonstrates Station Number, Status, Available bikes, and Available bike stands. Second, it displays the live weather information. It shows the condition, temperature, sensible temperature, and humidity. Third, it displays the prediction of the bike. The user can input the station and step (1 step = 10 minutes) to the model. The result will be shown in the screen. if the user does not select the station and the step, the station will be Blessington Street and the step will be 1 by default.

# Project Structure
First, the data will be collected from JCDecaux API to RDS MySQL database through scrapper every 10 minutes. However, the scrapper is hosted on Heroku. Second, the API that we created connects to RDS MySQL database. It transmits the data that the application needs. Besides, the API is hosted on Heroku. Third,