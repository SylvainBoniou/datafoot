import os
import pandas as pd
import streamlit as st
import json
import time

from src.scraping.utils_scraping import get_season, get_urls
from src.scraping.fbref_scraper import extract_fbref_match_table, extract_fbref_classement_table, extract_fbref_stat_squad_table
from src.processing.utils_processing import clean_fbref_matches

def process_league(league):
    # Create directories if missing
    os.makedirs("data/raw", exist_ok=True)
    os.makedirs("data/processed", exist_ok=True)

    url_current, url_previous = get_urls(league)
    season, last_season = get_season(league)

    df_classement = extract_fbref_classement_table(f"https://fbref.com/en/comps/13/Ligue-1-Stats")
    df_classement.to_csv(f"data/raw/{league['FBref slug']}_{season}_raw_data.csv", index=False)

    df_squad_stat = extract_fbref_stat_squad_table(f"https://fbref.com/en/comps/13/Ligue-1-Stats")
    df_squad_stat.to_csv(f"data/raw/{league['FBref slug']}_{season}_squad_stat_data.csv", index=False)

    # Scraping
    #df_matches_current = extract_fbref_match_table(url_current)
    #df_matches_current.to_csv(f"data/raw/{league['FBref slug']}_{season}_matches_raw_data.csv", index=False)

    #df_matches_previous = extract_fbref_match_table(url_previous)
    #df_matches_previous.to_csv(f"data/raw/{league['FBref slug']}_{last_season}_matches_raw_data.csv", index=False)

    # Cleaning
    #df_current = clean_fbref_matches(df_matches_current)
    #df_current.to_csv(f"data/processed/{league['FBref slug']}_{season}_matches.csv", index=False)

    #df_previous = clean_fbref_matches(df_matches_previous)
    #df_previous.to_csv(f"data/processed/{league['FBref slug']}_{last_season}_matches.csv", index=False)

def run_all_leagues():
    st.session_state["stop_pipeline"] = False
    with open("config/fbref_leagues.json", "r") as f:
        leagues = json.load(f)

    active_leagues = [lg for lg in leagues if lg.get("Active", False)]
    total = len(active_leagues)

    progress_bar = st.progress(0)
    status_text = st.empty()

    with st.expander("📜 Logs", expanded=True):
        log_area = st.empty()

    logs = []
    st.write(f"🚀 Début du chargement pour **{total}** championnat(s)...")

    for idx, league in enumerate(active_leagues, start=1):
        if st.session_state.get("stop_pipeline", False):
            status_text.write("⏹ Processus stoppé par l'utilisateur.")
            break

        league_name = league.get(league.get("FBref slug"))
        status_text.text(f"Chargement du championnat : {idx}/{total} : {league_name}")

        try:
            process_league(league)
            msg = f"✅ {league_name} processus terminé."
        except Exception as e:
            msg = f"❌ {league_name} Erreur: {e}"

        logs.append(msg)
        log_area.text("\n".join(logs))
        progress_bar.progress(idx / total)

        # 👇 Keep Streamlit refreshing the UI (important for the button Stop)
        time.sleep(0.1)

    status_text.text("✅ Processus OK")
    st.success("Chargement terminée.")