"""Tableau de bord des rappels de produits. — Lot C, Adam.

Commanditaire : association de défense des consommateurs. Le lecteur visé est
un consommateur, pas un responsable qualité : les titres énoncent un constat en
français courant et chaque limite est affichée dans la page, pas reléguée au
notebook (TB-04, TB-05).

Lancement, depuis la racine du dépôt :

    streamlit run app/dashboard.py

Ce module n'effectue aucun calcul : il appelle `src/indicators.py` (QC-03) et
filtre une seule fois en amont, de sorte que les filtres s'appliquent à toutes
les vues (TB-02). Le contrat d'interface est dans docs/contrat-de-donnees.md.
Tant qu'un indicateur n'est pas livré, son bloc affiche le lot qui le doit.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

RACINE = Path(__file__).resolve().parent.parent
if str(RACINE) not in sys.path:
    sys.path.insert(0, str(RACINE))

from src import indicators  # noqa: E402  (après l'ajout de la racine au chemin)

SOURCE = "RappelConso V2 — DGCCRF, DGAL, DGEC, DGPR — Licence Ouverte Etalab 2.0"

LIMITES = [
    "On mesure les rappels **publiés**, pas les défauts réels : une hausse peut "
    "venir d'un renforcement des contrôles.",
    "RappelConso a ouvert en **avril 2021**. Les 238 fiches antérieures sont "
    "écartées ; janvier 2021 n'en compte que 8, juillet 2021 en compte 964 — "
    "une reprise de stock, pas un pic saisonnier.",
    "L'année en cours est **incomplète** : la comparer aux années pleines "
    "fabrique une baisse qui n'existe pas.",
    "Cinq champs (nature juridique, compensation, conduites, distributeurs, "
    "zone) sont vides pour **2 192 fiches**. Les indicateurs qui les utilisent "
    "affichent leur propre dénominateur.",
    "Un classement de marques nomme des entreprises réelles. Une marque très "
    "présente en rayon a mécaniquement plus de rappels : ce n'est **pas** un "
    "palmarès de la dangerosité.",
]

GRIS = "#8a8a8a"
NOIR = "#1a1a1a"


# --------------------------------------------------------------------------
# Rendu
# --------------------------------------------------------------------------


def figure_barres(donnees: pd.DataFrame, colonne_libelle: str, colonne_valeur: str,
                  axe_x: str, mise_en_avant: int = 1) -> plt.Figure:
    """Barres horizontales triées, la plus longue en haut et en foncé."""
    donnees = donnees.iloc[::-1]
    hauteur = max(2.2, 0.38 * len(donnees))
    figure, axe = plt.subplots(figsize=(7, hauteur))
    couleurs = [NOIR] * len(donnees)
    for i in range(len(donnees) - mise_en_avant):
        couleurs[i] = GRIS
    axe.barh(donnees[colonne_libelle].astype(str), donnees[colonne_valeur], color=couleurs)
    axe.set_xlabel(axe_x)
    for bord in ("top", "right"):
        axe.spines[bord].set_visible(False)
    for i, valeur in enumerate(donnees[colonne_valeur]):
        axe.text(valeur, i, f" {valeur:,.0f}".replace(",", " "), va="center", fontsize=9)
    axe.margins(x=0.14)
    figure.tight_layout()
    return figure


def figure_annees(donnees: pd.DataFrame) -> plt.Figure:
    """Colonnes par année, la part due à la listeria en foncé à la base."""
    figure, axe = plt.subplots(figsize=(7, 3.4))
    annees = donnees["annee"].astype(str)
    axe.bar(annees, donnees["rappels"], color="#d2d2d2", label="autres risques")
    axe.bar(annees, donnees["listeria"], color=NOIR, label="dont listeria")
    axe.set_ylabel("rappels publiés (nombre de fiches)")
    axe.set_xlabel("année de publication")
    axe.legend(frameon=False, fontsize=8)
    for bord in ("top", "right"):
        axe.spines[bord].set_visible(False)
    for i, ligne in enumerate(donnees.itertuples()):
        axe.text(i, ligne.rappels, f"{ligne.rappels:,.0f}".replace(",", " "),
                 ha="center", va="bottom", fontsize=9)
    figure.tight_layout()
    return figure


def bloc(titre: str, sous_titre: str, lot: str):
    """Ouvre un bloc de question ; rend un conteneur pour y poser le graphique."""
    st.markdown(f"#### {titre}")
    st.caption(sous_titre)
    return st.container(), lot


def a_livrer(lot: str, fonction: str) -> None:
    """Message affiché tant que l'indicateur n'est pas écrit, au lieu du graphique."""
    st.info(
        f"Indicateur `{fonction}` non encore livré — **{lot}**. "
        "La structure, les titres et les limites de ce bloc sont en place ; "
        "le graphique apparaîtra sans modifier ce fichier.",
        icon="⏳",
    )


# --------------------------------------------------------------------------
# Page
# --------------------------------------------------------------------------


def main() -> None:
    st.set_page_config(page_title="Rappels de produits", layout="wide")

    st.title("Rappels de produits : qu'est-ce qui est rappelé, pourquoi, et qu'en faire ?")
    st.caption(
        "État des lieux pour les consommateurs — "
        f"source : {SOURCE}"
    )

    try:
        rappels = indicators.charge_rappels()
    except FileNotFoundError:
        st.warning(
            "**La table nettoyée n'existe pas encore.** "
            "Elle est produite par le lot A (`src/cleaning.py`), dont le contrat "
            "est fixé dans `docs/contrat-de-donnees.md`.",
            icon="⚠️",
        )
        st.code("python src/download.py\npython src/cleaning.py", language="bash")
        st.stop()

    # --- Filtres, appliqués une seule fois pour toutes les vues (TB-02) ---
    with st.sidebar:
        st.header("Filtres")
        annees = sorted(rappels["annee"].unique())
        debut, fin = st.select_slider(
            "Période de publication",
            options=annees,
            value=(annees[0], annees[-1]),
        )
        categories = sorted(rappels["categorie_produit"].dropna().unique())
        retenues = st.multiselect(
            "Familles de produits",
            options=categories,
            default=categories,
            help="Vide = toutes les familles.",
        )
        st.caption("Les deux filtres s'appliquent à l'ensemble des vues.")

    filtre = rappels["annee"].between(debut, fin)
    if retenues:
        filtre &= rappels["categorie_produit"].isin(retenues)
    vue = rappels[filtre]

    if vue.empty:
        st.warning("Aucun rappel ne correspond à ces filtres.", icon="🔍")
        st.stop()

    # --- Indicateurs clés en tête (TB-01) ---
    try:
        cles = indicators.indicateurs_cles(vue).iloc[0]
        colonnes = st.columns(5)
        colonnes[0].metric("Rappels publiés", f"{cles['total']:,.0f}".replace(",", " "),
                           f"{cles['evolution_12_mois']:+.0f} % sur 12 mois")
        colonnes[1].metric("Dans votre assiette", f"{cles['part_alimentaire']:.0f} %")
        colonnes[2].metric("Risque n° 1", str(cles["risque_n1"]),
                           f"{cles['part_risque_n1']:.0f} % des rappels", delta_color="off")
        colonnes[3].metric("Remboursement prévu", f"{cles['part_rembourse']:.0f} %")
        colonnes[4].metric("Rappel tardif (> 1 mois)", f"{cles['part_tardif']:.0f} %")
    except NotImplementedError:
        a_livrer("lot B, Feriel", "indicateurs_cles")

    st.divider()

    gauche, droite = st.columns(2)

    # --- Q1 : familles de produits (comparaison entre catégories, TB-03) ---
    with gauche:
        st.markdown("#### Trois rappels sur quatre concernent un aliment")
        st.caption("Part de chaque famille dans les rappels retenus — Q1")
        try:
            par_categorie = indicators.rappels_par_categorie(vue)
            st.pyplot(figure_barres(par_categorie, "categorie", "rappels",
                                    "rappels publiés (nombre de fiches)"))
            st.caption(f"Source : {SOURCE}")
        except NotImplementedError:
            a_livrer("lot B, Feriel", "rappels_par_categorie")

    # --- Q2 : risques ---
    with droite:
        st.markdown("#### Deux bactéries pèsent un quart des rappels")
        st.caption("Risques encourus les plus fréquents — un rappel peut en citer plusieurs — Q2")
        try:
            risques = indicators.risques_dominants(vue, n=8)
            st.pyplot(figure_barres(risques, "risque", "rappels",
                                    "rappels publiés (nombre de fiches)"))
            st.caption(f"Source : {SOURCE}")
        except NotImplementedError:
            a_livrer("lot B, Feriel", "risques_dominants")

    gauche, droite = st.columns(2)

    # --- Q3 : marques ---
    with gauche:
        st.markdown("#### Les marques de distributeur arrivent en tête")
        st.caption("Marques les plus souvent rappelées, hors mentions vides — Q3")
        try:
            marques = indicators.marques_recurrentes(vue, n=10)
            st.pyplot(figure_barres(marques, "marque", "rappels",
                                    "rappels publiés (nombre de fiches)"))
            st.caption(
                "Une enseigne rappelle pour toute sa gamme : un rang élevé signale "
                "une forte présence en rayon, pas une marque plus dangereuse. "
                f"Source : {SOURCE}"
            )
        except NotImplementedError:
            a_livrer("lot B, Feriel", "marques_recurrentes")

    # --- Q4 : évolution dans le temps (TB-03) ---
    with droite:
        st.markdown("#### Le nombre de rappels n'augmente pas ; la listeria s'est stabilisée")
        st.caption("Rappels par année, et part due à la listeria — Q4")
        try:
            par_annee = indicators.rappels_par_annee(vue)
            st.pyplot(figure_annees(par_annee))
            st.caption(f"Source : {SOURCE}")
        except NotImplementedError:
            a_livrer("lot B, Feriel", "rappels_par_annee")

    st.divider()

    # --- Limites, dans la page et non dans le notebook (TB-05) ---
    with st.expander("Ce que ces chiffres ne disent pas", expanded=True):
        for limite in LIMITES:
            st.markdown(f"- {limite}")

    # --- Export des données filtrées (TB-08, souhaité) ---
    st.download_button(
        "Télécharger les rappels affichés (CSV)",
        data=vue.to_csv(index=False).encode("utf-8"),
        file_name="rappels_filtres.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()
