import streamlit as st
import pandas as pd
from io import StringIO


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


def stream_app():
    st.title("Westminster bag delivery processing")
    with st.expander("Instructions"):
        st.markdown(
            """
        Step 1: Upload a bag-delivery csv file.\n
        Step 2: The application will then extract the area number from the
        `"Transport Area Code"` field, and assign it to a new field called 
        `"Transport Area Number"`\n
        Step 3: Click on `"Press to Download"` to download the csv file with 
        the new `"Transport Area Number" field.\n
        Step 4: View the location of the stops in the uploaded file on the map.\n
        Step 5: View the table directly in the app.\n
        """
        )
    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        stringio = StringIO(uploaded_file.getvalue().decode("unicode_escape"))
        dataframe = pd.read_csv(uploaded_file)
        dataframe = (
            dataframe.dropna(subset=["Site Latitude"])
            .dropna(subset=["Site Longitude"])
            .dropna(subset=["Transport Area Code"])
        )
        dataframe = dataframe.assign(
            transport_area=dataframe["Transport Area Code"].str[:1]
        ).rename(columns={"transport_area": "Transport Area Number"})
        dataframe_plot = dataframe.rename(
            columns={"Site Latitude": "lat", "Site Longitude": "lon"}
        )
        st.download_button(
            "Press to Download",
            dataframe.to_csv(index=False).encode("utf-8"),
            "modified_file.csv",
            "text/csv",
            key="download-csv",
        )
        st.map(dataframe_plot)
        st.write(dataframe)


if check_password():
    stream_app()
