from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from random import shuffle

def generate_hashtags(message):
    message = message.lower()
    text_tokens = word_tokenize(message)

    for word in text_tokens:
        if word.isalpha() != True:
            text_tokens.remove(word)

    tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]

    hashtags = ''
    for word in tokens_without_sw:
        word = '#' + word
        hashtags += ' ' + word
    return hashtags

def shuffle_list(list):
    list = list[:]
    shuffle(list)
    return list