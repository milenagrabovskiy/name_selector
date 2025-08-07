#main.py is 'brain' of flask
import flask
from flask import Flask, render_template, jsonify, session
import random
import logging as logger

app = Flask(__name__)

app.logger.setLevel(logger.DEBUG)

app.secret_key = "secret_key"

names_list = ['Aaron', 'Biniam', 'Boni', 'Jackie', 'Kidi',
                      'Kobby', 'Milena', "Maithreyi", "Mylardo", 'Tatiana',
                      'Tesfaye', 'UD', 'Yousef']

@app.route('/') # like 'home page'
def index():
    return render_template('index.html')

@app.route('/get-name')
def get_name():
    last_called = session.get('last_called')

    while True:
        random_name = random.choice(names_list)
        if random_name != last_called:
            break

    session['last_called'] = random_name #session is storing memory. so this way same name wont be picked twice in a row
    app.logger.debug(f"Currently selected: {random_name}") #was not seeing logging msg before adding 'app'
    return jsonify({'name': random_name}) #to send data to browser as json


if __name__ == '__main__': #this will run flask server
    app.run(host='0.0.0.0', debug=True)



