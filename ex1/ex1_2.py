import nltk

nltk.download('wordnet')
from nltk.corpus import wordnet as wn


def get_syn(word):
    return wn.synsets(str(word), pos=wn.NOUN)


if __name__ == '__main__':
    get_syn('rock')
