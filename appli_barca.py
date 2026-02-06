import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from datetime import datetime, date, timedelta
import openpyxl
import re
from mplsoccer import VerticalPitch, pitch, PyPizza, add_image, FontManager
import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
from matplotlib.patches import RegularPolygon, Arrow, Circle
from matplotlib.colors import ListedColormap
from mycolorpy import colorlist as mcp
from urllib.request import urlopen
from PIL import Image

#configuration de l'application
st.set_page_config(
    page_title=" DataFoot",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

df = pd.read_excel('./data/player_profiles.xlsx')
df_player = pd.read_csv("./data/test//player_event_data_shot_laliga2023_24.csv")
df_shot = pd.read_csv("./data/test/live_event_data_shot_laliga2023_24.csv")

#menu
with st.sidebar:
  selected = option_menu(
    menu_title = "Menu",
    options = ["Equipe","Joueur","Data coach"],
    icons = ["people-fill","person-arms-up"],
    menu_icon = "cast",
    default_index = 0,
    styles={
          "container": {"background-color": "#fafafa"},
          "icon": {"color": "orange", "font-size": "25px"},
          "nav-link": { "font-family": "Oxanium, sans-serif","font-size": "700", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
          "nav-link-selected": {"background-color": "rgb(0, 13, 68)"},
    }
  )

#menu Equipe
if selected == "Equipe":
    t1, t2 = st.columns((0.1, 1))
    t1.image('./data/ligue1.png', width = 120)
    t2.header('Analyse de la performance collective ',divider="gray")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Sélection de l'equipe
        df.sort_values('Equipe', ascending=True, inplace=True)
        liste_equipe = df['Equipe'].unique()
        equipe = st.selectbox('Choisissez une équipe', liste_equipe, index=None,
                                 placeholder="Sélectionnez une équipe...")

#menu Joueur
if selected == "Joueur":
    t1, t2 = st.columns((0.1, 1))
    t1.image('./data/ligue1.png', width = 120)
    t2.header('Analyse de la performance individuel ',divider="gray")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Sélection de l'equipe
        df.sort_values('Equipe', ascending=True, inplace=True)
        liste_equipe = df['Equipe'].unique()
        equipe = st.selectbox('Choisissez une équipe', liste_equipe, index=None,
                                 placeholder="Sélectionnez une équipe...")

    with col2:
        # Sélection de l'equipe
        df_joueurs = df[(df['Equipe'] == equipe)]
        df_joueurs.sort_values('Nom', ascending=True, inplace=True)
        liste_joueur = df_joueurs['Nom'].unique()
        joueur = st.selectbox('Choisissez un joueur', liste_joueur, index=None,
                                 placeholder="Sélectionnez une joueur...")
        df_joueurs = df[(df['Nom'] == joueur)]

    if joueur != "Sélectionnez une joueur...":

        a, b, c, d, e, f = st.columns(6)
        a.metric("Age 📆", int(df_joueurs['Age'].str[:2]), border=True)
        b.metric("Poste 👕", str(df_joueurs['position'].str[:2]),  border=True)
        c.metric("Buts 🥅", df_joueurs['Buts'],  border=True)
        d.metric("Passes décisive ⚽", df_joueurs['Passes décisives'],  border=True)
        e.metric("Cartons jaunes 🟨", df_joueurs['cards_yellow'], border=True)
        f.metric("Cartons rouges 🟥", df_joueurs['cards_red'],  border=True)

        st.divider()
        # pizza
        #image
        #URL = "https://raw.githubusercontent.com/andrewRowlinson/mplsoccer-assets/main/fdj_cropped.png"
        #fdj_cropped = Image.open(urlopen(URL))

        df_but_top10 = df.nlargest(20, 'Buts')
        df_but_top10 = df_but_top10[['Buts']].mean()
        df_xg_top10 = df.nlargest(20, 'xG sans pénalty')
        df_xg_top10 = df_xg_top10[['xG sans pénalty']].mean()
        df_xa_top10 = df.nlargest(20, 'pass_xa')
        df_xa_top10 = df_xa_top10[['pass_xa']].mean()
        df_passed_top10 = df.nlargest(20, 'Passes décisives')
        df_passed_top10 = df_passed_top10[['Passes décisives']].mean()
        df_cipa_top10 = df.nlargest(20, 'crosses_into_penalty_area')
        df_cipa_top10 = df_cipa_top10[['crosses_into_penalty_area']].mean()

        df_pct_top10 = df.nlargest(20, 'passes_pct')
        df_pct_top10 = df_pct_top10[['passes_pct']].mean()
        df_pp_top10 = df.nlargest(20, 'Passes progressives')
        df_pp_top10 = df_pp_top10[['Passes progressives']].mean()
        df_cp_top10 = df.nlargest(20, 'Conduites progressives')
        df_cp_top10 = df_cp_top10[['Conduites progressives']].mean()
        df_pift_top10 = df.nlargest(20, 'passes_into_final_third')
        df_pift_top10 = df_pift_top10[['passes_into_final_third']].mean()
        df_cift_top10 = df.nlargest(20, 'carries_into_final_third')
        df_cift_top10 = df_cift_top10[['carries_into_final_third']].mean()

        df_chal_top10 = df.nlargest(20, 'challenge_tackles_pct')
        df_chal_top10 = df_chal_top10[['challenge_tackles_pct']].mean()
        df_tacle_top10 = df.nlargest(20, 'Tacles')
        df_tacle_top10 = df_tacle_top10[['Tacles']].mean()
        df_inter_top10 = df.nlargest(20, 'Interceptions')
        df_inter_top10 = df_inter_top10[['Interceptions']].mean()
        df_bpasse_top10 = df.nlargest(20, 'blocked_passes')
        df_bpasse_top10 = df_bpasse_top10[['blocked_passes']].mean()
        df_contre_top10 = df.nlargest(20, 'Contres')
        df_contre_top10 = df_contre_top10[['Contres']].mean()

        # parameter list
        params = [
            "Buts", "npxG", "xA",
            "Passes D", "\nPenalty Area\nEntries",
            "% passes réussies", "Progressive\nPasses", "Progressive\nCarries",
            "Final 1/3 Passes", "Final 1/3 Carries",
            "% duels gagnés", "Tacles",
            "Interceptions", "Passes\ncontrées", "Contres"
        ]

        df_joueurs = df_joueurs[['Buts','xG sans pénalty','pass_xa','Passes décisives','crosses_into_penalty_area','passes_pct','Passes progressives','Conduites progressives','passes_into_final_third','carries_into_final_third','challenge_tackles_pct','Tacles','Interceptions','blocked_passes','Contres']]

        but = int(df_joueurs['Buts'].iloc[0]/df_but_top10*100)
        xg = int(df_joueurs['xG sans pénalty'].iloc[0] / df_xg_top10 * 100)
        xa = int(df_joueurs['pass_xa'].iloc[0] / df_xa_top10 * 100)
        passe_d = int(df_joueurs['Passes décisives'].iloc[0] / df_passed_top10 * 100)
        cipa = int(df_joueurs['crosses_into_penalty_area'].iloc[0] / df_cipa_top10 * 100)

        pct = int(df_joueurs['passes_pct'].iloc[0]/df_pct_top10*100)
        pp = int(df_joueurs['Passes progressives'].iloc[0] / df_pp_top10 * 100)
        cp = int(df_joueurs['Conduites progressives'].iloc[0] / df_cp_top10 * 100)
        pift = int(df_joueurs['passes_into_final_third'].iloc[0] / df_pift_top10 * 100)
        cift = int(df_joueurs['carries_into_final_third'].iloc[0] / df_cift_top10 * 100)

        chal = int(df_joueurs['challenge_tackles_pct'].iloc[0]/df_chal_top10*100)
        tacle = int(df_joueurs['Tacles'].iloc[0] / df_tacle_top10 * 100)
        inter = int(df_joueurs['Interceptions'].iloc[0] / df_inter_top10 * 100)
        bpasse = int(df_joueurs['blocked_passes'].iloc[0] / df_bpasse_top10 * 100)
        contre = int(df_joueurs['Contres'].iloc[0] / df_contre_top10 * 100)

        values_df = [
            but, xg, xa, passe_d, cipa,
            pct, pp, cp, pift, cift,
            chal, tacle, inter, bpasse, contre
        ]

        # color for the slices and text
        slice_colors = ["#1A78CF"] * 5 + ["#FF9300"] * 5 + ["#D70232"] * 5
        text_colors = ["#000000"] * 10 + ["#F2F2F2"] * 5

        # instantiate PyPizza class
        baker = PyPizza(
            params=params,                  # list of parameters
            background_color="#EBEBE9",     # background color
            straight_line_color="#EBEBE9",  # color for straight lines
            straight_line_lw=1,             # linewidth for straight lines
            last_circle_lw=0,               # linewidth of last circle
            other_circle_lw=0,              # linewidth for other circles
            inner_circle_size=20            # size of inner circle
        )

        # plot pizza
        fig, ax = baker.make_pizza(
            values_df,                          # list of values
            figsize=(8, 8.5),                # adjust figsize according to your need
            color_blank_space="same",        # use same color to fill blank space
            slice_colors=slice_colors,       # color for individual slices
            value_colors=text_colors,        # color for the value-text
            value_bck_colors=slice_colors,   # color for the blank spaces
            blank_alpha=0.4,                 # alpha for blank-space colors
            kwargs_slices=dict(
                edgecolor="#F2F2F2", zorder=2, linewidth=1
            ),                               # values to be used when plotting slices
            kwargs_params=dict(
                color="#000000", fontsize=11,
                 va="center"
            ),                               # values to be used when adding parameter
            kwargs_values=dict(
                color="#000000", fontsize=11,
                 zorder=3,
                bbox=dict(
                    edgecolor="#000000", facecolor="cornflowerblue",
                    boxstyle="round,pad=0.2", lw=1
                )
            )                                # values to be used when adding parameter-values
        )

        # add title
        fig.text(
            0.515, 0.975, str(joueur) +" - "+ str(equipe), size=16,
            ha="center",  color="#000000"
        )

        # add subtitle
        fig.text(
            0.515, 0.953,
            "Classement par rapport au TOP 20 | Saison 2024-25",
            size=13,
            ha="center", color="#000000"
        )

        # add credits
        CREDIT_1 = "data: fbref"

        fig.text(
            0.99, 0.02, f"{CREDIT_1}", size=9,
            color="#000000",
            ha="right"
        )

        # add text
        fig.text(
            0.34, 0.925, "Attaque          Possession       Défense", size=14,
            color="#000000"
        )

        # add rectangles
        fig.patches.extend([
            plt.Rectangle(
                (0.31, 0.9225), 0.025, 0.021, fill=True, color="#1a78cf",
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.462, 0.9225), 0.025, 0.021, fill=True, color="#ff9300",
                transform=fig.transFigure, figure=fig
            ),
            plt.Rectangle(
                (0.632, 0.9225), 0.025, 0.021, fill=True, color="#d70232",
                transform=fig.transFigure, figure=fig
            ),
        ])

        # add image
        # ax_image = add_image(
        #     fdj_cropped, fig, left=0.4478, bottom=0.4315, width=0.13, height=0.127
        # )   # these values might differ when you are plotting

        a, b = st.columns(2)

        a.pyplot(fig)

        # Sélection uniquement des colonnes 'playerId' et 'name'
        player = df_player[['playerId', 'name']].drop_duplicates()

        # Jointure des données de tirs avec les données des joueurs
        df_shot = df_shot.merge(player, how='left', on='playerId')

        # Afficher toutes les colonnes
        pd.set_option('display.max_columns', None)

        # Regroupement par identifiant et nom de joueur pour calculer:
        # - le nombre total d'événements (tirs)
        # - le nombre d'événements marquants (buts)
        player_stats = df_shot.groupby(['playerId', 'name']).agg(
            total_events=('playerId', 'count'),  # Compte le nombre total d'événements
            scoring_events=('type', lambda x: (x == 'Goal').sum())  # Compte uniquement les buts
        ).reset_index()

        # Tri des joueurs par nombre total d'événements (tirs) en ordre décroissant
        player_stats.sort_values(by="total_events", ascending=False, inplace=True)

        # Filtrage pour garder uniquement les joueurs avec plus de 30 tirs
        player_stats = player_stats[player_stats["total_events"] > 30]

        # Calcul du ratio de conversion (buts/tirs)
        player_stats["ratio"] = player_stats["scoring_events"] / player_stats["total_events"]

        # Extraction du nom de famille (en prenant le deuxième élément après séparation par espace)
        player_stats["last_name"] = player_stats["name"].str.split().str[1]

        # Définition des couleurs pour la visualisation
        green = '#69f900'
        red = '#ff4b44'
        blue = '#00a0de'
        violet = '#a369ff'
        bg_color = '#f5f5f5'
        line_color = '#000000'
        col1 = '#ff4b44'
        col2 = '#00a0de'

        # Couleurs pour l'équipe à domicile et à l'extérieur
        hcol = col1  # Couleur équipe domicile
        acol = col2  # Couleur équipe extérieure

        # Création d'un terrain vertical UEFA avec des paramètres personnalisés
        pitch = VerticalPitch(pitch_type='uefa',  # Type de terrain selon les normes UEFA
                              line_zorder=2,  # Ordre d'affichage des lignes
                              pitch_color='#1e4259',  # Couleur de fond du terrain
                              pad_bottom=0.5,  # Espacement en bas (terrain s'étend légèrement sous la ligne médiane)
                              half=False,  # Terrain complet (pas de demi-terrain)
                              goal_type='box',  # Style de représentation des buts
                              goal_alpha=0.8)  # Transparence des buts

        # Dessiner le terrain
        fig, ax = pitch.draw(figsize=(8, 8.5))

        # Sélection des colonnes pertinentes pour l'analyse des tirs
        sub_df_shot = df_shot[['id', 'x', 'y', 'type', 'playerId', 'name', 'match_id']]

        # Redimensionnement des coordonnées pour les adapter à la taille d'un terrain de football
        # Les coordonnées d'origine sont multipliées par des facteurs d'échelle pour correspondre
        # aux dimensions du terrain visualisé avec mplsoccer
        sub_df_shot['x'] = df_shot['x'] * 100 * 1.05  # Mise à l'échelle des coordonnées x
        sub_df_shot['y'] = df_shot['y'] * 100 * 0.68  # Mise à l'échelle des coordonnées y

        # Redessiner le terrain
        fig, ax = pitch.draw(figsize=(8, 8.5))

        # Création d'une carte de chaleur hexagonale des tirs sur le terrain
        # Les zones avec plus de tirs seront plus rouges (cmap='Reds')
        hexmap = pitch.hexbin(sub_df_shot.x, sub_df_shot.y,
                              edgecolors='black',  # Bordure noire des hexagones
                              gridsize=(10, 10),  # Taille de la grille (10x10 hexagones)
                              cmap='Reds',  # Palette de couleurs (rouge)
                              ax=ax)  # Axe sur lequel dessiner

        # Génération de points aléatoires pour créer une grille hexagonale couvrant tout le terrain
        hx = np.random.uniform(low=0, high=105, size=5000)  # Coordonnées x aléatoires (largeur du terrain = 105)
        hy = np.random.uniform(low=0, high=68, size=5000)  # Coordonnées y aléatoires (hauteur du terrain = 68)

        # Création de la grille hexagonale et stockage de sa référence
        # Cela servira de base pour notre analyse spatiale
        hexmap = pitch.hexbin(hx, hy, edgecolors='black', gridsize=(10, 10), cmap='Reds', ax=ax)

        # Extraction des centres des hexagones dans un DataFrame
        # Chaque hexagone aura un identifiant unique (hexbin_id) et des coordonnées (x,y)
        hexbin_df = pd.DataFrame(hexmap.get_offsets()).reset_index().rename(columns={"index": "hexbin_id", 0: "y", 1: "x"})


        # Fonction pour associer chaque tir au centre d'hexagone le plus proche
        def add_closest_center(random_points, centers):
            # Extraction des coordonnées sous forme de tableaux numpy
            random_coords = random_points[['x', 'y']].values
            center_coords = centers[['x', 'y']].values
            center_ids = centers['hexbin_id'].values

            # Calcul de la matrice de distances entre chaque tir et chaque centre d'hexagone
            distances = cdist(random_coords, center_coords, 'euclidean')

            # Identification de l'indice du centre d'hexagone le plus proche pour chaque tir
            closest_center_indices = np.argmin(distances, axis=1)

            # Ajout de nouvelles colonnes au DataFrame des tirs
            result = random_points.copy()
            result['hexbin_id'] = center_ids[closest_center_indices]  # ID de l'hexagone le plus proche
            result['hex_x'] = centers.iloc[closest_center_indices]['x'].values  # Coordonnée x du centre
            result['hex_y'] = centers.iloc[closest_center_indices]['y'].values  # Coordonnée y du centre
            result['min_distance'] = [distances[i, closest_center_indices[i]] for i in
                                      range(len(random_points))]  # Distance au centre

            return result


        # Application de la fonction pour associer chaque tir à l'hexagone le plus proche
        sub_df_shot = add_closest_center(sub_df_shot, hexbin_df)

        # Regroupement des données de tirs par joueur et par hexagone
        stat_df_shot = sub_df_shot.groupby(['playerId', 'hexbin_id', 'hex_x', 'hex_y']).agg(
            shot_event=('id', 'count'),  # Nombre total de tirs
            n_match=('match_id', 'nunique'),  # Nombre de matchs uniques
            goal_event=('type', lambda x: (x == 'Goal').sum())  # Nombre de buts marqués
        ).reset_index()

        # Calcul des métriques de performance
        stat_df_shot['event_per_game'] = stat_df_shot['shot_event'] / stat_df_shot['n_match']  # Tirs par match
        stat_df_shot['goal_per_shot'] = stat_df_shot['goal_event'] / stat_df_shot[
            'shot_event']  # Taux de conversion (buts/tirs)

        # Calcul des percentiles de performance pour chaque hexagone
        # Cela permet d'identifier les performances relatives dans chaque zone
        percentiles = stat_df_shot.groupby('hexbin_id').agg(
            # Percentiles pour les tirs par match (20%, 40%, 50%, 60%, 80%)
            event_per_game_20=('event_per_game', lambda x: x.quantile(0.20)),
            event_per_game_40=('event_per_game', lambda x: x.quantile(0.40)),
            event_per_game_50=('event_per_game', lambda x: x.quantile(0.50)),
            event_per_game_60=('event_per_game', lambda x: x.quantile(0.60)),
            event_per_game_80=('event_per_game', lambda x: x.quantile(0.80)),
            # Percentiles pour le taux de conversion (20%, 40%, 50%, 60%, 80%)
            goal_per_shot_20=('goal_per_shot', lambda x: x.quantile(0.20)),
            goal_per_shot_40=('goal_per_shot', lambda x: x.quantile(0.40)),
            goal_per_shot_50=('goal_per_shot', lambda x: x.quantile(0.50)),
            goal_per_shot_60=('goal_per_shot', lambda x: x.quantile(0.60)),
            goal_per_shot_80=('goal_per_shot', lambda x: x.quantile(0.80))
        )

        # Classement des joueurs au sein de chaque hexagone selon le nombre de tirs par match
        # Un rang plus petit (1) indique une meilleure performance
        stat_df_shot['event_per_game_rank'] = stat_df_shot.groupby('hexbin_id')['event_per_game'].rank(method='min',
                                                                                                       ascending=False)

        # Classement des joueurs au sein de chaque hexagone selon le taux de conversion
        stat_df_shot['goal_per_shot_rank'] = stat_df_shot.groupby('hexbin_id')['goal_per_shot'].rank(method='min',
                                                                                                     ascending=False)

        # Calcul du rang en pourcentage (échelle 0-100)
        # Plus le pourcentage est élevé, meilleure est la performance relative
        stat_df_shot['event_per_game_pct_rank'] = stat_df_shot.groupby('hexbin_id')['event_per_game'].rank(method='max',
                                                                                                           pct=True) * 100
        stat_df_shot['goal_per_shot_pct_rank'] = stat_df_shot.groupby('hexbin_id')['goal_per_shot'].rank(method='max',
                                                                                                         pct=True) * 100

        # Recherche d'un joueur par nom (partiel) - ici 'lewan' pour Lewandowski
        player_to_find = 'lewan'
        # Récupération de l'identifiant du joueur dont le nom contient 'lewan' (insensible à la casse)
        idp = player[player['name'].str.contains(player_to_find, case=False, regex=True)]['playerId'].values[0]

        # Récupération du nom complet du joueur à partir de son identifiant
        player_name = player[player['playerId'] == idp]['name']

        # Nettoyage du nom : suppression des chiffres (qui pourraient être présents dans la chaîne)
        player_name = re.sub(r'\d', '', player_name.to_string())

        # Suppression des espaces en début et fin de chaîne
        player_name = player_name.strip()

        # Filtrage des statistiques pour ne garder que celles du joueur sélectionné
        stat_player = stat_df_shot[stat_df_shot['playerId'] == idp]

        # Extraction des tirs ayant abouti à un but pour ce joueur
        player_goal = sub_df_shot[(sub_df_shot['playerId'] == idp) & (sub_df_shot['type'] == "Goal")]

        # Extraction des tirs n'ayant pas abouti à un but pour ce joueur
        player_shot = sub_df_shot[(sub_df_shot['playerId'] == idp) & (sub_df_shot['type'] != "Goal")]

        # Sélection des colonnes pertinentes pour l'analyse de l'efficacité par zone
        stat_player = stat_player[['hex_x', 'hex_y', 'goal_per_shot', 'goal_per_shot_pct_rank']]

        # Ajustement du classement en pourcentage : si le taux de conversion est 0,
        # le rang en pourcentage est également mis à 0
        stat_player['goal_per_shot_pct_rank'] = np.where(stat_player['goal_per_shot'] == 0, 0,
                                                         stat_player['goal_per_shot_pct_rank'])


        def add_title(fig, ax, title, sub_title, league, stat, colorlist):
            """
            Ajoute des titres, sous-titres et annotations personnalisées à une figure matplotlib.

            Paramètres:
            - fig: objet figure matplotlib
            - ax: objet axes matplotlib
            - title: texte du titre principal (nom du joueur)
            - sub_title: texte du sous-titre (type d'analyse)
            - league: nom de la ligue pour le sous-titre
            - stat: statistique visualisée (pour la légende)
            - colorlist: liste de couleurs pour le style
            """
            font = 'serif'

            # Titre principal et sous-titres - positionnés en haut
            fig.text(x=0.51, y=0.95, s=f"{title}", va="bottom", ha="center",
                     fontsize=24, color="black", font=font, weight="bold")

            fig.text(x=0.51, y=0.91, s=f"{sub_title} | {league} ",
                     va="bottom", ha="center", fontsize=14, font=font)

            # Placement de la légende en haut - juste sous le sous-titre
            y_height = 0.875  # Position verticale des hexagones

            # Ajout d'hexagones pour représenter l'échelle de couleur dans la légende
            annot_x = [0.43, 0.47, 0.51, 0.55, 0.59]  # Positions horizontales des hexagones

            # Création des hexagones de légende avec les couleurs correspondantes
            for x, color in zip(annot_x, colorlist):
                hex_annotation = RegularPolygon((x, y_height), numVertices=6, radius=0.02,
                                                edgecolor='#f4f4f4', fc=color, lw=0.5,
                                                transform=fig.transFigure)
                fig.patches.append(hex_annotation)

            # Ajout de flèches pour les indicateurs de direction
            arrow1 = Arrow(x=0.62, y=y_height, dx=0.04, dy=0, width=0.015,
                           color='#242424', transform=fig.transFigure)

            # Création des cercles pour la légende des tirs/buts
            y_circle = 1480
            # Cercle blanc avec contour rouge (buts)
            circle1 = Circle(xy=(830, y_circle), radius=12, facecolor='white', edgecolor='red')
            # Cercle blanc avec contour rouge et hachures (tirs non convertis)
            circle2 = Circle(xy=(1020, y_circle), radius=12, facecolor='white', edgecolor='red', hatch='///////')

            # Ajout des flèches et cercles à la figure
            fig.patches.extend([arrow1, circle1, circle2])

            # Ajout des textes explicatifs pour les cercles
            fig.text(x=0.495, y=y_height - 0.049, s="Buts", weight='bold', va="bottom", ha="center", fontsize=10, font=font)
            fig.text(x=0.575, y=y_height - 0.049, s="Tirs", weight='bold', va="bottom", ha="center", fontsize=10, font=font)



            higher_text = fig.text(0.68, y_height, "zone efficace", weight='bold',
                                   fontsize=12, font=font, va='center')

            return  higher_text

        # Génération d'une palette de couleurs personnalisée
        colorlist = mcp.gen_color(cmap='Blues_r', n=6)[::-1][1:]  # Utilisation de la palette "Blues" inversée
        # Prend 5 couleurs (exclut la première après inversion)
        custom_cmap = ListedColormap(colorlist)  # Création d'une palette de couleurs matplotlib à partir de la liste

        # Détermination des valeurs min et max pour l'échelle de couleur
        # Ces valeurs serviront à calibrer la carte de chaleur
        vmin = stat_player['goal_per_shot_pct_rank'].min()  # Valeur minimale du classement en pourcentage
        vmax = stat_player['goal_per_shot_pct_rank'].max()  # Valeur maximale du classement en pourcentage

        # Configuration du terrain de football
        pitch = VerticalPitch(
            pitch_type='uefa',  # Type de terrain selon les normes UEFA
            line_zorder=2,  # Ordre d'empilement des lignes du terrain
            pitch_color='#f5f5f5',  # Couleur de fond du terrain (gris clair)
            pad_bottom=0.5,  # Espace supplémentaire en bas du terrain
            half=True,  # Afficher seulement la moitié offensive du terrain
            goal_type='box',  # Style de représentation des buts
            goal_alpha=0.8  # Transparence des buts
        )

        ##########################################
        # PARTIE 1: CRÉATION DE LA VISUALISATION
        ##########################################

        # Création de la figure et des axes
        fig, ax = plt.subplots(figsize=(8, 8.5))
        fig.set_facecolor('#f5f5f5')  # Fond gris clair

        # Ajustement de l'espace en haut pour le titre et la légende
        plt.subplots_adjust(top=0.8)

        # Dessin du terrain de football
        pitch.draw(ax=ax)

        # Création de la carte de chaleur hexagonale
        # Cette visualisation montre l'efficacité du joueur selon les zones du terrain
        hexbin = pitch.hexbin(
            stat_player.hex_x, stat_player.hex_y,  # Positions des hexagones
            C=stat_player.goal_per_shot_pct_rank,  # Valeurs pour la coloration (classement percentile)
            ax=ax,
            edgecolors='#f4f4f4',  # Couleur des bordures
            gridsize=(10, 10),  # Taille de la grille d'hexagones
            cmap=custom_cmap,  # Palette de couleurs personnalisée
            vmin=vmin,  # Valeur minimale pour l'échelle
            vmax=vmax,  # Valeur maximale pour l'échelle
            reduce_C_function=np.mean  # Fonction d'agrégation
        )

        ##########################################
        # PARTIE 2: AJOUT DES TIRS ET BUTS
        ##########################################

        # Visualisation des buts marqués
        scatter = pitch.scatter(
            player_goal.x, player_goal.y,  # Coordonnées exactes des buts
            ax=ax,
            s=90,  # Taille des points
            color='white',  # Couleur de remplissage
            alpha=0.8,  # Transparence
            edgecolors='red',  # Couleur de bordure
            marker='o',  # Forme (cercle)
            linewidth=0.5,  # Épaisseur de la bordure
            zorder=2  # Ordre d'affichage (au-dessus de la carte)
        )

        # Visualisation des tirs non convertis en buts (avec hachures)
        scatter = pitch.scatter(
            player_shot.x, player_shot.y,  # Coordonnées des tirs
            ax=ax,
            s=90,  # Taille des points
            color='white',  # Couleur de remplissage
            alpha=0.8,  # Transparence
            edgecolors='red',  # Couleur de bordure
            marker='o',  # Forme (cercle)
            hatch='///////',  # Motif de hachures pour distinguer des buts
            linewidth=0.5,  # Épaisseur de la bordure
            zorder=2  # Ordre d'affichage
        )

        # Remarque: Ce scatter plot suivant semble redondant (même chose que le premier)
        # Il s'agit peut-être d'une erreur ou d'une intention de superposition
        scatter = pitch.scatter(
            player_goal.x, player_goal.y,  # Mêmes coordonnées que précédemment
            ax=ax,
            s=90,  # Taille des points
            color='white',  # Couleur de remplissage
            alpha=0.8,  # Transparence
            edgecolors='red',  # Couleur de bordure
            marker='o',  # Forme (cercle)
            linewidth=0.5,  # Épaisseur de la bordure
            zorder=2  # Ordre d'affichage
        )

        ##########################################
        # PARTIE 3: FINALISATION ET AJOUT DE LA PHOTO
        ##########################################

        # Ajout du titre et des légendes avec la fonction personnalisée
        add_title(fig, ax, joueur, "Tirs tentés", "Saison 2024-2025", "stat", colorlist)

        # Import des outils pour ajouter une image
        from matplotlib.offsetbox import OffsetImage, AnnotationBbox

        # Ajout de la photo du joueur en bas à droite
        image_path = './data/test/250002096.png'  # Chemin vers l'image du joueur
        position = (1, 0)  # Position (coin inférieur droit)
        zoom = 0.25  # Zoom de l'image
        alpha = 1.0  # Opacité de l'image
        img = plt.imread(image_path)  # Lecture de l'image

        # Création d'un objet pour l'image
        imagebox = OffsetImage(img, zoom=zoom, alpha=alpha)

        # Création d'une boîte d'annotation pour placer l'image
        ab = AnnotationBbox(
            imagebox,
            position,
            xycoords='axes fraction',
            box_alignment=(1.0, 0.0),  # Alignement en bas à droite
            frameon=False  # Sans cadre
        )

        # Ajout de l'annotation à l'axe
        ax.add_artist(ab)

        # Affichage de la carte hexagonale
        b.pyplot(plt)

    # menu Data coach
if selected == "Data coach":
    col1, col2, col3 = st.columns(3)


