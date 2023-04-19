import pickle
import re
from random import choices
from markov_chain_lyric import MarkovChain

with open('markov_chain_artist_model.pkl', 'rb') as inp:
    model_dict = pickle.load(inp)
    print(list(model_dict.keys()))