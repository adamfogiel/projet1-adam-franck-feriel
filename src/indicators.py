"""Calcul des indicateurs. — Lot B, Feriel.

Ce module est appelé par le notebook **et** par le tableau de bord (exigence
QC-03). Un indicateur calculé directement dans le notebook ou dans Streamlit,
et pas ici, finira recodé deux fois et les deux versions divergeront.

Chaque fonction prend la table nettoyée et rend un DataFrame prêt à afficher.
Un indicateur est défini sans ambiguïté : formule, périmètre, unité.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
TABLE_NETTOYEE = RACINE / "data" / "processed" / "rappels.parquet"


def charge_rappels() -> pd.DataFrame:
    """Point d'entrée unique vers la table nettoyée, pour le notebook et le dashboard."""
    if not TABLE_NETTOYEE.exists():
        raise FileNotFoundError(
            f"{TABLE_NETTOYEE.name} absent. Lancer : python src/download.py "
            "puis python src/cleaning.py"
        )
    return pd.read_parquet(TABLE_NETTOYEE)


def rappels_par_mois(df: pd.DataFrame) -> pd.DataFrame:
    """TODO Feriel — nombre de fiches distinctes par mois (question Q3).

    Compter des fiches distinctes, pas des lignes : une fiche peut apparaître
    plusieurs fois. Le mois en cours est incomplet et doit être exclu ou
    signalé, sinon la courbe montre une chute qui n'existe pas.
    """
    raise NotImplementedError


def rappels_par_categorie(df: pd.DataFrame) -> pd.DataFrame:
    """TODO Feriel — répartition par catégorie de produit (question Q1)."""
    raise NotImplementedError


def categorie_par_annee(df: pd.DataFrame) -> pd.DataFrame:
    """TODO Feriel — croisement catégorie × année (EF-04).

    Rendre aussi la part de chaque catégorie dans le total annuel : les volumes
    bruts ne sont pas comparables d'une année à l'autre si le nombre total de
    rappels change (EF-07).
    """
    raise NotImplementedError


def motifs_dominants(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """TODO Feriel — motifs de rappel les plus fréquents (question Q2).

    `motif_rappel` est du texte libre : le comptage dépend entièrement de la
    normalisation retenue, qui doit être écrite dans docs/decisions.md.
    """
    raise NotImplementedError


def marques_recurrentes(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """TODO Feriel — marques les plus souvent rappelées (question Q4).

    Le résultat nomme des entreprises réelles. Il est rendu avec ses limites :
    une marque très présente en rayon a mécaniquement plus de rappels, et ce
    classement ne mesure pas une dangerosité.
    """
    raise NotImplementedError
