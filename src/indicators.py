"""Calcul des indicateurs. — Lot B, Feriel.

Ce module est appelé par le notebook **et** par le tableau de bord (exigence
QC-03). Un indicateur calculé directement dans le notebook ou dans Streamlit,
et pas ici, finira recodé deux fois et les deux versions divergeront.

Les signatures ci-dessous sont celles du contrat d'interface
(docs/contrat-de-donnees.md, 27/11). Elles ont été posées par le chef de projet
pour que le tableau de bord puisse être écrit sans attendre ; **les corps
restent à écrire par le lot B**. Les anciennes fonctions, qui renvoyaient aux
questions Q1 à Q5 abandonnées depuis, ont été retirées.

Chaque fonction reçoit le DataFrame **déjà filtré** par période et par
catégorie : les filtres sont appliqués une seule fois, en amont (TB-02).
Un indicateur est défini sans ambiguïté : formule, périmètre, unité.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
TABLE_NETTOYEE = RACINE / "data" / "processed" / "rappels.parquet"

#: Fiches dont les cinq champs métier sont renseignés, sur le jeu complet.
#: Tout indicateur qui touche la compensation, les conduites, la nature
#: juridique ou la zone filtre d'abord sur `fiche_complete`.
PERIMETRE_METIER = 17071


def charge_rappels() -> pd.DataFrame:
    """Point d'entrée unique vers la table nettoyée, pour le notebook et le dashboard."""
    if not TABLE_NETTOYEE.exists():
        raise FileNotFoundError(
            f"{TABLE_NETTOYEE.name} absent. Lancer : python src/download.py "
            "puis python src/cleaning.py"
        )
    return pd.read_parquet(TABLE_NETTOYEE)


def indicateurs_cles(df: pd.DataFrame) -> pd.DataFrame:
    """TODO lot B — une ligne, les cinq chiffres affichés en tête du tableau de bord.

    Colonnes attendues : `total`, `evolution_12_mois`, `part_alimentaire`,
    `risque_n1`, `part_risque_n1`, `part_rembourse`, `part_tardif`.

    `evolution_12_mois` compare les douze derniers mois aux douze précédents,
    jamais l'année civile en cours à une année pleine. `part_rembourse` et
    `part_tardif` se calculent sur `fiche_complete`, et leur dénominateur est
    affiché à côté du chiffre : 17 071 et non 19 025.
    """
    raise NotImplementedError


def rappels_par_annee(df: pd.DataFrame) -> pd.DataFrame:
    """TODO lot B — une ligne par année (EF-04, agrégation temporelle).

    Colonnes attendues : `annee`, `rappels`, `listeria`, `part_listeria`.

    Compter des fiches distinctes, pas des lignes. L'année en cours est
    incomplète : elle est renvoyée mais doit être signalée à l'affichage,
    sinon la dernière colonne montre une chute qui n'existe pas.
    """
    raise NotImplementedError


def rappels_par_categorie(df: pd.DataFrame) -> pd.DataFrame:
    """TODO lot B — une ligne par catégorie, triée (EF-04, agrégation par catégorie).

    Colonnes attendues : `categorie`, `rappels`, `part`.

    La part est indispensable : l'alimentaire pèse les trois quarts du jeu et
    les volumes bruts ne se comparent pas d'une période à l'autre (EF-07).
    """
    raise NotImplementedError


def sous_categories(df: pd.DataFrame, categorie: str, n: int = 15) -> pd.DataFrame:
    """TODO lot B — les n premières sous-catégories d'une famille donnée.

    Colonnes attendues : `sous_categorie`, `rappels`.

    C'est le grain utile sous les 74 % de l'alimentaire : sans lui, la
    répartition par catégorie se résume à une seule barre.
    """
    raise NotImplementedError


def risques_dominants(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """TODO lot B — les n risques les plus fréquents (EF-04).

    Colonnes attendues : `risque`, `rappels`, `part`.

    `risques` est une colonne de listes : la dépiler avant de compter, sinon
    « listeria|salmonella » devient un troisième risque qui n'existe pas. La
    somme des parts dépasse donc 100 %, et l'affichage doit le dire.
    """
    raise NotImplementedError


def marques_recurrentes(df: pd.DataFrame, n: int = 15) -> pd.DataFrame:
    """TODO lot B — les n marques les plus souvent rappelées (EF-04).

    Colonnes attendues : `marque`, `rappels`, `categorie_dominante`,
    `risque_dominant`.

    Les mentions vides (`sans marque`, 1 743 fiches, et `/`, 89 fiches) sont
    mises à nul par le lot A et doivent rester exclues ici : traitées comme des
    marques, elles occupent les deux premières places.

    Le résultat nomme des entreprises réelles. Il est rendu avec ses limites :
    une marque très présente en rayon a mécaniquement plus de rappels, et ce
    classement ne mesure pas une dangerosité.
    """
    raise NotImplementedError
