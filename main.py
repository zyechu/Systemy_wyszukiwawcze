import string
import streamlit as st
import morfeusz2
import nltk
import pandas as pd
import SessionState


st.title("Morfeus and python integration")
nouns = []
adjectives = []
verbs = []
markers_df = None
column_names = ["Wykładnik formy", "Lemat", "Znacznik morfosyntaktyczny", "Klasyfikacja nazw własnych", "Kwalifikatory"]
VERBS_SYMBOLS = ["fin", "praet"]
NOUNS_SYMBOLS = ["subst", "depr"]
ADJECTIVES_SYMBOLS = ["adj", "adja", "adjp"]
GRADES_OF_ADJECTIVES = {"equal": "pos", "higher": "com", "top": "sup"}

# nltk.download('punkt')


def analyse_sentence(text):
    morfeusz_object = morfeusz2.Morfeusz(praet='composite')
    analysys = morfeusz_object.analyse(text)
    for i, j, interp in analysys:
        # print(i,j,interp)
        get_verbs(interp)
        get_nouns(interp)
        get_adjectives(interp)


def generate_markers(word):
    generator = []
    morfeusz_object = morfeusz2.Morfeusz(praet='composite')
    analysys = morfeusz_object.analyse(word)
    for interp in analysys:
        generator.append(interp)
    return generator


def tokenize(text):
    tokens = nltk.word_tokenize(text.lower())
    return tokens


def remove_punctuation(tokenized_text):
    tech_list = []
    for word in tokenized_text:
        if word not in string.punctuation:
            tech_list.append(word)
    return tech_list


def get_verbs(inter_tuple):
    is_verb = any(symbol in inter_tuple[2] for symbol in VERBS_SYMBOLS)
    if is_verb:
        verbs.append(inter_tuple)


def get_nouns(inter_tuple):
    is_noun = any(symbol in inter_tuple[2] for symbol in NOUNS_SYMBOLS)
    if is_noun:
        nouns.append(inter_tuple)


def get_adjectives(inter_tuple):
    is_adjective = any(symbol in inter_tuple[2] for symbol in ADJECTIVES_SYMBOLS)
    if is_adjective:
        adjectives.append(inter_tuple)


def split_verbs_to_future_and_past(verbs_list):
    future_forms = []
    past_forms = []
    past_df = None
    future_df = None
    for idx, row in verbs_list.iterrows():
        if row["Znacznik morfosyntaktyczny"].split(":")[0] == "fin":
            values_list = row.values.tolist()
            future_forms.append(values_list)
        elif row["Znacznik morfosyntaktyczny"].split(":")[0] == "praet":
            values_list = row.values.tolist()
            past_forms.append(values_list)
    if len(future_forms) != 0:
        future_df = pd.DataFrame(future_forms)
        future_df.columns = column_names
    if len(past_forms) != 0:
        past_df = pd.DataFrame(past_forms)
        past_df.columns = column_names
    return past_df, future_df


def gradation_of_adjectives(adjectives_list):
    equal_forms = []
    equal_df = None
    higher_forms = []
    higher_df = None
    top_forms = []
    top_df = None
    for idx, row in adjectives_list.iterrows():
        if GRADES_OF_ADJECTIVES["equal"] in row["Znacznik morfosyntaktyczny"].split(":"):
            values_list = row.values.tolist()
            equal_forms.append(values_list)
        elif GRADES_OF_ADJECTIVES["higher"] in row["Znacznik morfosyntaktyczny"].split(":"):
            values_list = row.values.tolist()
            higher_forms.append(values_list)
        elif GRADES_OF_ADJECTIVES["top"] in row["Znacznik morfosyntaktyczny"].split(":"):
            values_list = row.values.tolist()
            top_forms.append(values_list)
    if len(equal_forms) != 0:
        equal_df = pd.DataFrame(equal_forms)
        equal_df.columns = column_names
    if len(higher_forms) != 0:
        higher_df = pd.DataFrame(higher_forms)
        higher_df.columns = column_names
    if len(top_forms) != 0:
        top_df = pd.DataFrame(top_forms)
        top_df.columns = column_names
    return equal_df, higher_df, top_df


user_input = st.text_area("Wprowadź tekst", "")
col1, col2 = st.beta_columns(2)
if col1.button("Analizuj tekst"):
    del markers_df
    analyse_sentence(user_input)
    verbs_df = pd.DataFrame(verbs)
    if not verbs_df.empty:
        st.write("Czasowniki")
        verbs_df.columns = column_names
        st.write(verbs_df)
        past, future = split_verbs_to_future_and_past(verbs_df)
        if isinstance(past, pd.DataFrame) and not past.empty:
            st.write("Czasowniki w czasie przeszłym")
            st.write(past)
        if isinstance(future, pd.DataFrame) and not future.empty:
            st.write("czasowniki w czasie nieprzeszłym")
            st.write(future)
    nouns_df = pd.DataFrame(nouns)
    if not nouns_df.empty:
        st.write("Rzeczowniki")
        nouns_df.columns = column_names
        st.write(nouns_df)
    adjectives_df = pd.DataFrame(adjectives)
    if not adjectives_df.empty:
        st.write("Przymiotniki")
        adjectives_df.columns = column_names
        st.write(adjectives_df)
        equal, higher, top = gradation_of_adjectives(adjectives_df)
        if isinstance(equal, pd.DataFrame) and not equal.empty:
            st.write("Przymiotniki w stopniu równym")
            st.write(equal)
        if isinstance(higher, pd.DataFrame) and not higher.empty:
            st.write("Przymiotniki w stopniu wyższym")
            st.write(higher)
        if isinstance(top, pd.DataFrame) and not top.empty:
            st.write("Przymiotniki w stopniu najwyższym")
            st.write(top)


if col2.button("Generuj znaczniki"):
    del verbs
    del nouns
    del adjectives
    if len(user_input.split(" ")) != 1:
        st.error("Proszę podać jeden lemat")
    else:
        markers = []
        generator_output = generate_markers(user_input)
        for output in generator_output:
            markers.append(list(output[2]))
        markers_df = pd.DataFrame(markers)
        markers_df.columns = column_names
        st.write(markers_df)
        # print(markers_df)

