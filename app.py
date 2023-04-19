from flask import Flask, render_template, jsonify
from random import choice
import pickle

app = Flask(__name__)

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'MarkovChain':
            from markov_chain_lyric import MarkovChain
            return MarkovChain
        return super().find_class(module, name)
markov_chain_model = CustomUnpickler(open('./markov_chain/markov_chain_artist_model.pkl', 'rb')).load() 
artist_list = list(markov_chain_model.keys())

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', artists=artist_list)

@app.route('/artist/generate/<string:artist>/<int:line_number>')
def generate(artist, line_number, methods=['GET']):
    if artist in markov_chain_model:
        markov_artist = markov_chain_model[artist]
        if not markov_artist.is_trained():
            markov_artist.train()
        return jsonify({'artist': ' '.join(w.capitalize() for w in artist.split()), 'lyric': markov_artist.generate(line_number)})
    return jsonify({'error': 'Artist not exist'})

@app.route('/artist/generate_random/<int:line_number>')
def generate_random(line_number, methods=['GET']):
    artist = choice(artist_list)
    markov_artist = markov_chain_model[artist]
    if not markov_artist.is_trained():
        markov_artist.train()
    return jsonify({'artist': ' '.join(w.capitalize() for w in artist.split()), 'lyric': markov_artist.generate(line_number)})
