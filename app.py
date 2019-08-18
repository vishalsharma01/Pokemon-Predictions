# Load Libraries
import pickle
import flask
import pandas as pd
import numpy as np
from flask import render_template
import app

app = flask.Flask(__name__)

#-------- MODEL GOES HERE -----------#
#
pokemon = pickle.load(open('pokemon.pkl', 'rb'))
pipe = pickle.load(open("pipe.pkl", "rb"))
names = pickle.load(open("name.pkl", "rb"))

#-------- ROUTES GO HERE -----------#

@app.route('/')
def page():
    return render_template('pokemon.html', name = names)

@app.route('/result', methods=['POST', 'GET'])
def result():


    '''Gets prediction using the HTML form'''
    if flask.request.method == 'POST':
        inputs = flask.request.form
        player1 = inputs['player 1']
        player2 = inputs['challenger']


        data = pd.DataFrame({
            'First_pokemon': [int(pokemon.loc[pokemon["Name"] == player1,"#"])],
            'Second_pokemon': [int(pokemon.loc[pokemon["Name"] == player2,"#"])]
        })

        data

        data_test = pd.merge(data, pokemon, how='left', left_on='First_pokemon', right_on='#')
        data_test = pd.merge(data_test, pokemon, how='left', left_on='Second_pokemon', right_on='#')

        pred = pipe.predict(data_test)[0]
        base_url = "https://img.pokemondb.net/artwork/"
        if pred == 1:
            pred = player1
            player_1_pic = player1.lower()+'.jpg'
            url = base_url+player_1_pic
        else:
            pred = player2
            player_2_pic = player2.lower()+'.jpg'
            url = base_url+player_2_pic
        return render_template('result.html', pred=pred, url=url)

if __name__ == '__main__':
    '''Connects to the server'''

    HOST = '127.0.0.1'
    PORT = 4000

    app.run(HOST, PORT, debug=True)
