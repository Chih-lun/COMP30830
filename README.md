# COMP30830 Software Engineering - Dublin Bikes (Group 8)
Application Address: http://34.254.238.187/

# Section 1. Introduction
This is an web application which is developed in Python Flask Framework. It includes the information of all bike stations in Dublin, the weather, and the prediction.

# Section 2. How this application works
There are 3 major parts in this application. First, it displays the locations of all stations. According to the station, it demonstrates Station Number, Status, Available bikes, and Available bike stands. Second, it displays the live weather information. It shows the condition, temperature, sensible temperature, and humidity. Third, it displays the prediction of the bike. The user can input the station and step (1 step = 10 minutes) to the model. The result will be shown in the screen. if the user does not select the station and the step, the station will be Blessington Street and the step will be 1 by default.

# Section 3. Project Structure
First, the data will be collected from JCDecaux API to RDS MySQL database through scrapper every 10 minutes. However, the scrapper is hosted on Heroku. Second, the API that we created connects to RDS MySQL database. It transmits the data that the application needs. Besides, the API is hosted on Heroku. Third, the backend integrates html, css, javascript, and machine learning model. Thus, the Flask application can serve the information mentioned in section 2.

# Section 4. AWS EC2
We host the website through AWS EC2. In the following are the instructions.

1. Connect to EC2.
2. Install python3, pip, nginx, gunicorn3
3. git clone https://github.com/Chih-lun/COMP30830.git
4. cd COMP30830
5. gunicorn3 main:app
