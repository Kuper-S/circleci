# Flask Weather App ☀️☔️
This is a Flask application that uses api to fetch forecast for the next week.

## Setup:
* Install Dependencies
* Install the requirements ```pip install -r requirements.txt```
* Move the ```flask.conf``` file to ```/etc/nginx/conf.d/```
* Move the ```flask.service``` file to ```/etc/systemd/system/```
* Start Nginx ```sudo systemctl start nginx```
* Start the service ```sudo systemctl start flask```

## Requirements:
* Listed in requirements.txt
* Nginx and Gunicorn installed.

## .env Variables:
* API_KEY - open weather api key (https://openweathermap.org/api). Save it in a file called .env

## Flask Application Structure:
```
.
├── countries.py
├── exceptions.py
├── README.md
├── requirements.txt
├── static
│   └── weather_front.css
├── templates
│   └── weather_front.html
├── weather_project.py
├── weather_utils.py
└── wsgi.py

2 directories, 9 files



/
└── etc
    ├── systemd
    │   └── system
    │       └── flask.service
    └── nginx
        └── conf.d
            └── flask.conf

```

## After The App Is Running:
* Go to the machine's ip (for example: ```127.0.0.1```).

##
>### How To Use?
> In order to change API you need to change the url and parsing in both functions
> inside the weather_utils.py along with the API key\s.\
> The APIs currently in use are OpenWeather in order to get the geo data (lon and lat),
> and OpenMeteo to get the data (does not require an API key, and is open source).

## References
* [Flask Official Website](http://flask.pocoo.org/)
