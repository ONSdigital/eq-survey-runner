from flask import Flask, render_template
from healthcheck import HealthCheck

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Wrap the app, and provide a healthcheck url
health = HealthCheck(app, "/healthcheck")

# Custom check function
def custom_check():
    return True, 'Peachy, Thanks!'

health.add_check(custom_check)

if __name__ == '__main__':
    app.run(debug=True)
