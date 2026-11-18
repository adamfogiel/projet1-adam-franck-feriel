"""Nettoyage et typage des fiches de rappel. — Lot A, Franck.

Ce module transforme les fichiers bruts de `data/raw/` en une table unique
`data/processed/rappels.parquet`, qui est le contrat sur lequel l'analyse
(`src/indicators.py`) et le tableau de bord (`app/dashboard.py`) travaillent.

Le schéma de cette table est figé dans `docs/decisions.md` avant d'être codé.
S'il doit changer, c'est une décision écrite, annoncée aux deux autres membres
le jour même : leurs travaux reposent dessus.

Chaque anomalie rencontrée est consignée dans `docs/anomalies.md`, y compris
celles qu'on choisit de ne pas traiter.

Usage :
    python src/cleaning.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
RAW_DIR = RACINE / "data" / "raw"
PROCESSED_DIR = RACINE / "data" / "processed"

# Séparateurs observés dans les champs multivalués (voir ANO-03).
SEPARATEURS = {
    "conduites_a_tenir_par_le_consommateur": "|",
    "modeles_ou_references": "¤",
}


def charge_brut(nom: str) -> pd.DataFrame:
    """Lit un fichier brut sans rien modifier, pour partir de la source telle quelle."""
    chemin = RAW_DIR / f"rappelconso_{nom}.parquet"
    if not chemin.exists():
        raise FileNotFoundError(
            f"{chemin.name} absent. Lancer d'abord : python src/download.py"
        )
    return pd.read_parquet(chemin)


def renomme_colonnes(df: pd.DataFrame) -> pd.DataFrame:
    """Corrige le nom fautif de la source (voir ANO-02)."""
    return df.rename(columns={"date_date_fin_commercialisation": "date_fin_commercialisation"})


def type_dates(df: pd.DataFrame) -> pd.DataFrame:
    """TODO Franck — typage des colonnes de dates.

    Points à traiter et à consigner dans docs/anomalies.md :
    - `date_publication` est un horodatage avec fuseau ; décider si on garde
      l'heure ou si on passe à la date seule, et le justifier. Les 19 263
      valeurs s'interprètent sans erreur (contrôlé le 18/11).
    - Les deux colonnes de dates de commercialisation sont remplies à 78 % et
      77 % : la question Q5 est donc traitable. Reste à vérifier qu'aucune date
      de fin n'est postérieure à la date de publication du rappel.
    - Le changement de format annoncé par le producteur en juillet 2024 n'a pas
      été retrouvé sur `date_publication`. Le contrôle reste à faire sur les
      deux colonnes de commercialisation avant de conclure.
    """
    raise NotImplementedError("typage des dates à écrire")


def normalise_marques(df: pd.DataFrame) -> pd.DataFrame:
    """TODO Franck — normalisation de `marque_produit`.

    Une même marque est écrite de plusieurs façons. La méthode retenue
    (minuscules, accents, ponctuation, regroupements manuels) est écrite dans
    docs/decisions.md AVANT d'être appliquée : elle change le classement des
    marques, donc une conclusion du livrable.
    """
    raise NotImplementedError("normalisation des marques à écrire")


def controle_unicite_fiches(df: pd.DataFrame) -> None:
    """Vérifie que le fichier des fiches garde une ligne par fiche.

    Mesuré le 18/11 : 19 263 valeurs distinctes de `numero_fiche` pour
    19 263 lignes. Le cahier des charges annonce une fiche répétée sur
    plusieurs lignes ; ce n'est pas le cas ici (voir anomalies.md). La source
    étant mise à jour chaque jour, ce contrôle doit rester en place : si
    l'hypothèse tombe, tous les comptages sont à revoir.
    """
    doublons = len(df) - df["numero_fiche"].nunique()
    if doublons:
        raise ValueError(
            f"{doublons} fiches apparaissent sur plusieurs lignes : "
            "l'hypothèse d'unicité ne tient plus, ouvrir une anomalie."
        )


def joint_produits(fiches: pd.DataFrame, produits: pd.DataFrame) -> pd.DataFrame:
    """TODO Franck — jointure EF-06 entre les deux fichiers.

    Clé : `numero_fiche` + `numero_version`. Structure mesurée le 18/11 :
    12 664 clés communes, 6 599 fiches sans aucun produit (34,3 %), zéro
    produit orphelin, et jusqu'à 88 produits pour une même fiche.

    Deux conséquences à traiter, pas à découvrir après coup :
    - une jointure interne perd un tiers des rappels (ANO-01) ;
    - une jointure gauche multiplie les lignes (ANO-02), donc tout comptage
      fait ensuite doit porter sur des fiches distinctes.

    Compter les lignes avant et après, et comparer au nombre attendu. Un
    `merge` dont on n'a pas vérifié le volume n'est pas contrôlé.
    """
    raise NotImplementedError("jointure à écrire")


def main() -> int:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    fiches = renomme_colonnes(charge_brut("fiches"))
    produits = renomme_colonnes(charge_brut("produits"))
    print(f"fiches   : {fiches.shape[0]} lignes, {fiches.shape[1]} colonnes")
    print(f"produits : {produits.shape[0]} lignes, {produits.shape[1]} colonnes")
    print("Nettoyage à écrire — voir les TODO de ce module.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
