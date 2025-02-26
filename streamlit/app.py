import streamlit as st
import requests
import json
import pandas as pd

st.title("Notícias mais prováveis de serem clicadas")
# st.write("Lista de notícias:")

with st.sidebar:
    st.header("Controls")
    if st.button("Update Database"):
        try:
            response = requests.get("http://data-pipeline:8000/updateDatabase")
            st.session_state.db_result = response.text
        except requests.exceptions.RequestException as e:
            st.session_state.db_result = f"Connection error: {str(e)}"

    if st.button("Materialize Feature"):
        try:
            response = requests.get("http://feast-globo:8001/materialize")
            st.session_state.materialize_result = response.text
        except requests.exceptions.RequestException as e:
            st.session_state.materialize_result = f"Connection error: {str(e)}"

if "db_result" in st.session_state:
    st.text_area("API Response", value=st.session_state.db_result, height=200)

st.subheader("Get news prediction")
st.write("Logged user: e7a6c843011a4823501fe0b297c0956d84db3d0f7399f4736336b6807d6a7339")

user_id = st.text_input("Enter user ID")

if st.button("Get predictions"):
    if user_id:
        try:
            response = requests.get(f"http://model:8002/getPrediction/{user_id}")
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data["predictions"])
                st.session_state.user_result = df
                st.session_state.raw_response = json.dumps(data, indent=2)
            else:
                st.session_state.user_result = None
                st.session_state.raw_response = f"Error: {response.status_code}"
        except requests.exceptions.RequestException as e:
            st.session_state.user_result = None
            st.session_state.raw_response = f"Connection error: {str(e)}"
    else:
        st.session_state.user_result = "Please enter the user id"

if "user_result" in st.session_state:
    if isinstance(st.session_state.user_result, pd.DataFrame):
        st.write("Predicted news data:")
        st.dataframe(st.session_state.user_result)  # Display as table
    st.text_area("Raw API Response", value=st.session_state.raw_response, height=200)

if "materialize_result" in st.session_state:
    st.write("Materialize result:")
    st.write(st.session_state.materialize_result)