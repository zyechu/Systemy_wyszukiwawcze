import string
import nltk
import re

from collections import Counter

class Analyser:
    def tokenize(self, text):
        tokens = nltk.word_tokenize(text.lower())
        return tokens

    def remove_punctuation(self, tokenized_text):
        tech_list = []
        for word in tokenized_text:
            if word not in string.punctuation:
                tech_list.append(word)
        return tech_list

    def count_word_occurrences(self, filtered_list):
        counts = Counter(filtered_list)
        return counts

    def count_whitespaces(self, text):
        space = 0
        for i in text:
            if i.isspace():
                space = space + 1
        return space

    def count_char(self,text):
        return len(text)

    def count_all_words(self, filtered_list):
        return len(filtered_list)

    def count_senteces(self, text):
        sents = re.split(r'[.!?]+', text)
        if sents[-1] == '':
            return len(sents)-1
        else:
            return len(sents)
