import pandas as pd
import re

def clean_fbref_matches(df: pd.DataFrame) -> pd.DataFrame:
    # 1️⃣ Standardize column names
    df = df.rename(columns=lambda x: x.strip())
    
    # Remove repeated header rows
    df = df[df["Score"] != "Score"].copy()
    df.reset_index(drop=True, inplace=True)

    # 2️⃣ Ensure unique column names (important for xG duplicates)
    df.columns = [
        f"{col}_{j}" if df.columns.duplicated()[j] else col
        for j, col in enumerate(df.columns)
    ]

    # 3️⃣ Identify useful columns
    cols = ['Date','Time', 'Home', 'Away', 'Score']
    
    # Detect xG columns (now uniquely named)
    xg_candidates = [col for col in df.columns if 'xG' in col]
    cols += xg_candidates
    
    # Keep only relevant columns
    df = df[cols]

    # 4️⃣ Filter out future matches (empty Score)
    df = df[df['Score'].str.contains(r'\d+[–-]\d+', na=False)].copy()

    # 5️⃣ Split score into home and away goals (as integers)
    df[['home_goal', 'away_goal']] = (
        df['Score']
        .str.extract(r'(\d+)[–-](\d+)')
        .astype(int)
    )
    df.drop(columns='Score', inplace=True)

    # 6️⃣ Rename xG columns if present
    if len(xg_candidates) == 2:
        df = df.rename(columns={xg_candidates[0]: 'xG_home', xg_candidates[1]: 'xG_away'})

    # 7️⃣ Reorder columns
    ordered_cols = ['Date','Time', 'Home', 'Away', 'home_goal', 'away_goal']
    if 'xG_home' in df.columns and 'xG_away' in df.columns:
        ordered_cols += ['xG_home', 'xG_away']

    return df[ordered_cols]
