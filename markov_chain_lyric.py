import re
from random import choices

# TRAINING / MODEL
class MarkovChain():
    def __init__(self, text):
        self._trained = False
        self.corpus = text
        self.wordfreq = {}
    
    def train(self):
        """Membangun model menggunakan markov chain berdasarkan teks lirik 
           yang telah diberikan
        """
        print('================Currently training================\n')
        for individual_song in self.corpus:
            bigram_tuple_list = self.bigrams(individual_song)
            for i in range(0, len(bigram_tuple_list) - 1):
                current = bigram_tuple_list[i]
                next = bigram_tuple_list[i+1]
                if current not in self.wordfreq:
                    self.wordfreq[current] = {}
                if next not in self.wordfreq[current]:
                    self.wordfreq[current][next] = 0
                self.wordfreq[current][next] += 1
        print('================Training done================\n')

        self._trained = True
    
    def generate_replacer(self, bigram):
        """Mengubah token yang telah diberikan ke dalam lirik
           ke huruf yang asli

           >>> self.generate_replacer(('Wow', '__COMMA__'))
           ','
        """
        if bigram[1] == '__NEWLINE__':
            return '\n'
        if bigram[1] == '__COMMA__':
            return ','
        if bigram[1] == '__QUESTION__':
            return '?'
        if bigram[1] == '__END__':
            return ''
        return bigram[1]

    def is_trained(self):
        """Jika model telah dilakukan training maka akan mengembalikan `True`"""
        return self._trained

    def generate(self, max_line_count=50):
        "Melakukan generate lagu berdasarkan teks yang telah diberikan"
        if not self._trained:
            raise Exception('Can\'t generate data if it haven\'t been trained')
        initial_state = ('__BEGIN__', '__BEGIN__')
        generated_sentance = []
        line_count = 0
        current = initial_state

        while True:
            next_dict_weight = self.wordfreq[current]
            next = choices(list(next_dict_weight.keys()), list(next_dict_weight.values()), k=1)[0]
            generated_sentance.append(next)
            if next[1] == '__NEWLINE__':
                line_count += 1
            if next[1] == '__END__':
                break
            if line_count >= max_line_count:
                break

            current = next            
        result = ' '.join(map(lambda x: self.generate_replacer(x), generated_sentance))
        result = result.replace(' ,', ',').replace(' ?', '?').replace(' \n', '\n')
        return re.sub(r'\n+', '\n', result)  # Replace \n+ string to single newline

    def bigrams(self, text):
        """Mengubah teks yang diberikan menjadi bigram languange model
           yang direpresentasikan dalam bentuk tuple
        """
        word_list = re.split(r'\s+', text)
        tuple_list = []
        for i in range(0, len(word_list) - 1):
            tuple_list.append(tuple(word_list[i : i+2]))
        return tuple_list