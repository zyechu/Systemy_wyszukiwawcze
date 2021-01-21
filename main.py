import pandas as pd
import streamlit as st

from morfeus_interface import MorfeusInterface

st.title("Morfeus and python integration")
nouns = []
adjectives = []
verbs = []
markers_df = None
user_input = st.text_area("Wprowadź tekst", "")
col1, col2 = st.beta_columns(2)
morfeus = MorfeusInterface()


def write_df_and_title_to_streamlit(df, title):
    st.write(title)
    st.write(df)


def check_if_variable_is_instance_of_pd_df_and_write_to_streamlit(variable_to_check, title):
    if isinstance(variable_to_check, pd.DataFrame) and not variable_to_check.empty:
        write_df_and_title_to_streamlit(variable_to_check, title)


if col1.button("Analizuj tekst"):
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
