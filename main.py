import pandas as pd
import streamlit as st

from morfeus_interface import MorfeusInterface
from analyser import Analyser

st.title("Morfeus and python integration")
nouns = []
adjectives = []
verbs = []
markers_df = None
user_input = st.text_area("Wprowadź tekst", "")
col1, col2 = st.beta_columns(2)
morfeus = MorfeusInterface()
analyser = Analyser()

def write_df_and_title_to_streamlit(df, title):
    st.write(title)
    st.table(df)


def check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(variable_to_check, title):
    if isinstance(variable_to_check, pd.DataFrame) and not variable_to_check.empty:
        write_df_and_title_to_streamlit(variable_to_check, title)


if col1.button("Analizuj tekst"):
    st.sidebar.title('Analiza częstości słów i znaków')
    clear_text = analyser.tokenize(user_input)
    clear_text = analyser.remove_punctuation(clear_text)
    word_counter = dict(analyser.count_word_occurrences(clear_text))
    dataframe = pd.DataFrame.from_dict(word_counter, orient='index')

    count_characters = analyser.count_char(user_input)
    count_whitespaces = analyser.count_whitespaces(user_input)
    count_all_words = analyser.count_all_words(clear_text)
    count_sents = analyser.count_senteces(user_input)

    st.sidebar.text(f"Liczba znaków: {count_characters}")
    st.sidebar.text(f"Liczba białych znaków: {count_whitespaces}")
    st.sidebar.text(f"Liczba słów: {count_all_words}")
    st.sidebar.text(f"Liczba zdań: {count_sents}")

    st.sidebar.text('Częstość słów')
    dataframe.columns = ['Licznik']
    dataframe['Częstość [%]'] = dataframe['Licznik']/sum(dataframe['Licznik'])
    dataframe['Częstość [%]'] = [round(x, 2) for x in dataframe['Częstość [%]']]
    dataframe = dataframe.sort_values(by=['Licznik'], ascending=False)
    st.sidebar.table(dataframe.style.format({'Częstość [%]':"{:.2%}"}))

    del markers_df

    verbs_df, nouns_df, adjectives_df = morfeus.analyse_sentence(user_input)
    if not verbs_df.empty:
        write_df_and_title_to_streamlit(verbs_df, "Czasowniki")
        past, future = morfeus.split_verbs_to_future_and_past(verbs_df)
        check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(past, "Czasowniki w czasie przeszłym")
        check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(future, "Czasowniki w czasie nieprzeszłym")
    if not nouns_df.empty:
        write_df_and_title_to_streamlit(nouns_df, "Rzeczowniki")
    if not adjectives_df.empty:
        write_df_and_title_to_streamlit(adjectives_df, "Przymiotniki")
        equal, higher, top = morfeus.gradation_of_adjectives(adjectives_df)
        check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(equal, "Przymiotniki w stopniu równym")
        check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(higher, "Przymiotniki w stopniu wyższym")
        check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(top, "Przymiotniki w stopniu najwyższym")

if col2.button("Generuj znaczniki"):
    del verbs
    del nouns
    del adjectives
    if len(user_input.split(" ")) != 1:
        st.error("Proszę podać jeden lemat")
    else:
        markers = []
        generator_output = morfeus.generate_markers(user_input)
        st.write(generator_output)
