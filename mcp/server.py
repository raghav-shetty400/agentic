from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/weather/<city>")
def weather(city):

    return jsonify({
        "city": city,
        "temp": "28C"
    })


if __name__ == "__main__":
    app.run(port=8000)
