import os
import json
from datetime import datetime
import streamlit as st
import pandas as pd

@st.cache_data
def load_data(league: str, season: str):
    file_path = f"data/processed/{league}_{season}_matches.csv"
    df = pd.read_csv(file_path)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Time"] = pd.to_datetime(df["Time"], errors="coerce")
    return df


@st.cache_data
def load_data_classement(league: str, season: str):
    file_path = f"data/raw/{league}_{season}_raw_data.csv"
    df = pd.read_csv(file_path)
    return df