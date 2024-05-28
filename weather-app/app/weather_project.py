from flask import Flask, render_template, request
import weather_utils
import exceptions


# Export weather api key
app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def load_home():
    if request.method == 'POST':
        location = request.form['location']
        try:
            data = weather_utils.get_weather_data(location)
            return render_template('weather_front.html', data=data)
        except exceptions.LocationError as error:
            return render_template('weather_front.html', error=error)
        except exceptions.DataError as error:
            return render_template('weather_front.html', error=error)

    return render_template('weather_front.html')


@app.errorhandler(404)
def error_handler(error):
    return render_template('weather_front.html', error=error)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
