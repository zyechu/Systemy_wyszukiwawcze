import string

import morfeusz2
import nltk
import pandas as pd


class MorfeusInterface():
    def __init__(self):
        self.column_names = ["Wykładnik formy", "Lemat", "Znacznik morfosyntaktyczny", "Klasyfikacja nazw własnych",
                             "Kwalifikatory"]
        self.VERBS_SYMBOLS = ["fin", "praet"]
        self.NOUNS_SYMBOLS = ["subst", "depr"]
        self.ADJECTIVES_SYMBOLS = ["adj", "adja", "adjp"]
        self.GRADES_OF_ADJECTIVES = {"equal": "pos", "higher": "com", "top": "sup"}
        self.MORPHOSYNTACTIC_MARKER = "Znacznik morfosyntaktyczny"
        self.morfeusz_object = morfeusz2.Morfeusz(praet='composite')
        self.nouns = []
        self.adjectives = []
        self.verbs = []

    def analyse_sentence(self, text):
        analysys = self.morfeusz_object.analyse(text)
        for i, j, interp in analysys:
            # print(i,j,interp)
            self.get_verbs(interp)
            self.get_nouns(interp)
            self.get_adjectives(interp)
        verbs_df_object = self.convert_list_to_df_with_columns_name(self.verbs)
        nouns_df_object = self.convert_list_to_df_with_columns_name(self.nouns)
        adjectives_df_object = self.convert_list_to_df_with_columns_name(self.adjectives)
        return verbs_df_object, nouns_df_object, adjectives_df_object

    def generate_markers(self, word):
        generator = []
        analysys = self.morfeusz_object.analyse(word)
        for i, j, interp in analysys:
            generator.append(interp)
        generator_df_object = self.convert_list_to_df_with_columns_name(generator)
        return generator_df_object

    def tokenize(self, text):
        tokens = nltk.word_tokenize(text.lower())
        return tokens

    def remove_punctuation(self, tokenized_text):
        tech_list = []
        for word in tokenized_text:
            if word not in string.punctuation:
                tech_list.append(word)
        return tech_list

    def get_verbs(self, inter_tuple):
        is_verb = any(symbol in inter_tuple[2] for symbol in self.VERBS_SYMBOLS)
        if is_verb:
            self.verbs.append(inter_tuple)

    def get_nouns(self, inter_tuple):
        is_noun = any(symbol in inter_tuple[2] for symbol in self.NOUNS_SYMBOLS)
        if is_noun:
            self.nouns.append(inter_tuple)

    def get_adjectives(self, inter_tuple):
        is_adjective = any(symbol in inter_tuple[2] for symbol in self.ADJECTIVES_SYMBOLS)
        if is_adjective:
            self.adjectives.append(inter_tuple)

    def convert_list_to_df_with_columns_name(self, list_to_convert):
        df_object = pd.DataFrame(list_to_convert)
        if len(list_to_convert) != 0:
            df_object.columns = self.column_names
        return df_object

    def check_length_and_return_df(self, list_to_check):
        df_object = []
        if len(list_to_check) != 0:
            df_object = self.convert_list_to_df_with_columns_name(list_to_check)
        return df_object

    def append_df_row_to_list(self, df_row, list_to_append):
        values_list = df_row.values.tolist()
        list_to_append.append(values_list)
        return list_to_append

    def split_verbs_to_future_and_past(self, verbs_list):
        future_forms = []
        past_forms = []
        for idx, row in verbs_list.iterrows():
            if row[self.MORPHOSYNTACTIC_MARKER].split(":")[0] == "fin":
                future_forms = self.append_df_row_to_list(row, future_forms)
            elif row[self.MORPHOSYNTACTIC_MARKER].split(":")[0] == "praet":
                past_forms = self.append_df_row_to_list(row, past_forms)
        future_df = self.check_length_and_return_df(future_forms)
        past_df = self.check_length_and_return_df(past_forms)
        return past_df, future_df

    def gradation_of_adjectives(self, adjectives_list):
        equal_forms = []
        higher_forms = []
        top_forms = []
        for idx, row in adjectives_list.iterrows():
            if self.GRADES_OF_ADJECTIVES["equal"] in row[self.MORPHOSYNTACTIC_MARKER].split(":"):
                equal_forms = self.append_df_row_to_list(row, equal_forms)
            elif self.GRADES_OF_ADJECTIVES["higher"] in row[self.MORPHOSYNTACTIC_MARKER].split(":"):
                higher_forms = self.append_df_row_to_list(row, higher_forms)
            elif self.GRADES_OF_ADJECTIVES["top"] in row[self.MORPHOSYNTACTIC_MARKER].split(":"):
                top_forms = self.append_df_row_to_list(row, top_forms)
        equal_df = self.check_length_and_return_df(equal_forms)
        higher_df = self.check_length_and_return_df(higher_forms)
        top_df = self.check_length_and_return_df(top_forms)
        return equal_df, higher_df, top_df
