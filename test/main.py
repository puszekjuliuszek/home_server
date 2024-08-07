from flask import Flask
from flask import render_template

# creates a Flask application
app = Flask(__name__)


@app.route("/")
def hello():
    message = "Hello, World"
    return render_template('index.html', message=message)

@app.route("/images")
def serve_image():
    message = "Image Route"
    return render_template('images.html', message=message)


# run the application
if __name__ == "__main__":
    app.run(debug=True)
