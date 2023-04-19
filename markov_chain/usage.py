# USAGE CODE
import pickle

class CustomUnpickler(pickle.Unpickler):
    def find_class(self, module, name):
        if name == 'MarkovChain':
            from markov_chain_lyric import MarkovChain
            return MarkovChain
        return super().find_class(module, name)

markov_chain_model = CustomUnpickler(open('./markov_chain_artist_model.pkl', 'rb')).load() 
artist_list = list(markov_chain_model.keys())

print(markov_chain_model['Eminem'].generate())
