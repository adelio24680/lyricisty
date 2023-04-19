import pandas as pd
import re
from random import choices
import pickle


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

# CLEANING DATA
def cleaning_data(df_lyric):
    """Melakukan cleaning pada dataset lirik cinta
    Menghilangkan baris yang ada null dan empty string
    """
    nan_value = float('NaN')
    df_lyric.replace('', nan_value, inplace=True)
    df_lyric.dropna(subset=['lyric'], inplace=True)
    df_lyric.head()

    return df_lyric

# PREPROCESSING DATA
def lowercase(lyric):
    """Mengubah seluruh lirik lagu menjadi huruf kecil"""
    return lyric.lower()

def make_begin(lyric):
    """Memulai dengan __BEGIN__ __BEGIN__ karena 
    menggunakan bigram languange model"""
    lyrics = lyric.strip().split('\n')
    if len(lyrics) > 0:
        lyrics[0] = '__BEGIN__ __BEGIN__ ' + lyrics[0]
    return '\n'.join(lyrics)

def make_end(lyric):
    """Mengakhiri lirik lagu dengan __END__ sebagai penanda
    bahwa lagu telah selesai"""
    lyrics = lyric.strip().split('\n')
    if len(lyrics) > 0:
        lyrics[-1] = lyrics[-1].replace('\n', '') + ' __END__'
    return '\n'.join(lyrics)

def remove_carriage_feed(lyric):
    """Terkadang data yang ada menggunakan newline jenis '\r\n'
       sehingga kami akan menghilangkannya
    """
    return lyric.replace('\r', '')

def make_newline_token(lyric):
    """Melakukan replace pada newline token dengan __NEWLINE__"""
    return lyric.replace('\n', ' __NEWLINE__ ')

def make_comma_token(lyric):
    """Melakukan replace pada tanda baca koma dengan __COMMA__"""
    return lyric.replace(',', ' __COMMA__ ')

def make_question_token(lyric):
    """Melakukan replace pada tanda baca koma dengan __COMMA__"""
    return lyric.replace('?', ' __QUESTION__ ')

def replace_raw_languange(lyric):
    """Dalam lirik lagu biasa terdapat lirik dengan penulisan yang bervariasi
       Sehingga akan direplace dengan kata baku supaya lebih konsisten dalam model
    """
    lyric.replace("s'lalu", 'selalu')
    lyric.replace("t'lah", 'telah')
    lyric.replace("'kan", 'akan')
    lyric.replace("'tuk", 'untuk')
    lyric.replace("'ku'", 'aku')
    return lyric

def remove_parentheses_word(lyric):
    """Di dalam lirik lagu biasanya terdapat kata seperti '(Lirik lagu)'
       Yang biasanya menandakan pengulangan. Kami akan menghilangkan kata
       tersebut
       >>> remove_parentheses_word('Hello World (Hello World)')
       'Hello World '
    """
    return re.sub(r'\([^)]*\)', '', lyric)

def remove_punctuation(lyric, punctuations=['.', '"']):
    """Menghilangkan tanda baca `punctuations` yang diinginkan
       dari lirik lagu `lyric`
    """
    for punc in punctuations:
        lyric = lyric.replace(punc, '')
    return lyric


if __name__ == '__main__':
    # LOADING DATA
    df_lyric = pd.read_csv('./markov_chain/cinta_lyrics.csv')

    # CLEANING DATA
    df_lyric = cleaning_data(df_lyric)

    # PREPROCESSING DATA
    df_lyric['artist'] = df_lyric['artist'].apply(lambda x: x.strip())
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: lowercase(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: make_begin(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: make_end(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: remove_carriage_feed(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: make_newline_token(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: make_comma_token(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: make_question_token(x))
    # df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: replace_raw_languange(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: remove_parentheses_word(x))
    df_lyric['lyric'] = df_lyric['lyric'].apply(lambda x: remove_punctuation(x))


    markov_artist_dict = dict()
    for artist in df_lyric['artist'].unique():
        print(artist, (df_lyric['artist'] == artist).sum())
        if (df_lyric['artist'] == artist).sum() >= 10:
            markov_artist_dict[artist] = MarkovChain((df_lyric.loc[df_lyric['artist'] == artist])['lyric'])
            markov_artist_dict[artist].train()

    with open('markov_chain_artist_model.pkl', 'wb') as outp:
        pickle.dump(markov_artist_dict, outp, pickle.HIGHEST_PROTOCOL)
