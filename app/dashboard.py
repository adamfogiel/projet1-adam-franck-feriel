"""Tableau de bord des rappels de produits. — Lot C, Adam.

Lancement :
    streamlit run app/dashboard.py

Exigences à couvrir (TB-01 à TB-06) :
- la page d'accueil répond à la question principale, 3 à 5 indicateurs en tête ;
- filtres période et catégorie, appliqués à toutes les vues ;
- une vue d'évolution temporelle et une vue de comparaison entre catégories ;
- chaque graphique porte un titre qui énonce le constat, des axes nommés avec
  leurs unités, et la source ;
- les limites des données sont visibles ici, pas seulement dans le notebook ;
- lancement en une commande, affichage en moins de 10 secondes.

Les calculs viennent de `src/indicators.py` : aucun indicateur n'est calculé
dans ce fichier (QC-03).
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src import indicators  # noqa: E402

SOURCE = (
    "Source : RappelConso V2, DGCCRF / DGAL / DGEC / DGPR, "
    "data.economie.gouv.fr, Licence Ouverte Etalab 2.0"
)

LIMITES = """
**Ce que ces chiffres ne disent pas.** Le jeu recense les rappels *publiés*,
pas les défauts de produits. Une hausse du nombre de fiches peut traduire un
renforcement des contrôles autant qu'une dégradation de la sécurité. Un
classement de marques reflète aussi leur présence en rayon.
"""

st.set_page_config(page_title="Rappels de produits", layout="wide")

st.title("Rappels de produits de consommation")
st.caption(SOURCE)

try:
    rappels = indicators.charge_rappels()
except FileNotFoundError as erreur:
    st.warning(str(erreur))
    st.info(
        "Le tableau de bord se lance mais n'a pas encore de données nettoyées. "
        "Le squelette est en place : filtres, vues et indicateurs à construire."
    )
    st.stop()

# TODO Adam — filtres période et catégorie dans la barre latérale (TB-02),
# appliqués à toutes les vues.

# TODO Adam — 3 à 5 indicateurs clés en tête de page (TB-01).

# TODO Adam — vue d'évolution temporelle et vue de comparaison (TB-03),
# titres qui énoncent le constat, axes nommés, barres partant de zéro (TB-04).

st.markdown("---")
st.markdown(LIMITES)
