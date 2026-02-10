from flask import Flask, render_template, request
import requests
import pickle

app = Flask(__name__)

# ===============================
# CONFIG
# ===============================
API_KEY = "aa0888d3a063d299825e755a28bd437c"

# Load trained ML model
with open("../model/model.sav", "rb") as f:
    model = pickle.load(f)

# ===============================
# HOME PAGE
# ===============================
@app.route("/")
def home():
    return render_template("home.html")

# ===============================
# WEATHER PAGE
# ===============================
@app.route("/weather", methods=["GET", "POST"])
def weather():
    weather_data = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")

        if city:
            try:
                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city}&appid={API_KEY}&units=metric"
                )
                response = requests.get(url)
                data = response.json()

                if data.get("cod") != 200:
                    error = "City not found. Please enter a valid city name."
                else:
                    weather_data = {
                        "city": data["name"],
                        "temperature": data["main"]["temp"],
                        "humidity": data["main"]["humidity"],
                        "pressure": data["main"]["pressure"],
                        "wind_speed": data["wind"]["speed"],
                        "condition": data["weather"][0]["description"].title()
                    }

            except Exception as e:
                error = "Error fetching weather data. Please try again."

    return render_template(
        "weather.html",
        weather_data=weather_data,
        error=error
    )

# ===============================
# ENERGY PREDICTION PAGE
# ===============================
@app.route("/predict", methods=["GET", "POST"])
def predict():
    prediction = None
    error = None

    if request.method == "POST":
        try:
            wind_speed = float(request.form.get("wind_speed"))
            theoretical_power = float(request.form.get("theoretical_power"))
            wind_direction = float(request.form.get("wind_direction"))

            prediction = round(
                model.predict([[wind_speed, theoretical_power, wind_direction]])[0],
                2
            )

        except Exception as e:
            error = "Invalid input. Please enter numeric values."

    return render_template(
        "predict.html",
        prediction=prediction,
        error=error
    )

# ===============================
# RUN APP
# ===============================
if __name__ == "__main__":
    app.run(debug=True)
