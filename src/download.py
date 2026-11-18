"""Récupération des deux jeux RappelConso V2 depuis data.economie.gouv.fr.

Deux jeux sont téléchargés, parce que la jointure EF-06 se fait entre eux :

- `rappelconso-v2-gtin-espaces` : une ligne par fiche de rappel. Les produits
  concernés sont empilés dans `identification_produits`, en multivalué.
- `rappelconso-v2-gtin-trie`   : une ligne par produit (colonne `gtin` en plus).
  Ce jeu exclut les produits sans code-barres, d'où un total différent.

Les fichiers bruts ne sont pas versionnés (voir .gitignore) : ce script les
reconstruit. Chaque téléchargement écrit un manifeste daté à côté du fichier,
pour que l'analyse reste rattachable à une version précise de la source.

Usage :
    python src/download.py            # télécharge ce qui manque
    python src/download.py --force    # retélécharge tout
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets"

# Chemins relatifs à la racine du dépôt : aucun chemin absolu dans le code (ET-04).
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

DATASETS = {
    "fiches": "rappelconso-v2-gtin-espaces",
    "produits": "rappelconso-v2-gtin-trie",
}

LICENCE = "Licence Ouverte Etalab 2.0"
PRODUCTEURS = "DGCCRF, DGAL, DGEC, DGPR"


def compte_lignes(dataset_id: str) -> int:
    """Nombre de lignes annoncé par l'API, pour contrôler le téléchargement."""
    url = f"{BASE_URL}/{dataset_id}/records?limit=1"
    with urllib.request.urlopen(url, timeout=60) as reponse:
        return json.load(reponse)["total_count"]


def telecharge(dataset_id: str, destination: Path) -> None:
    """Export Parquet complet du jeu, écrit sur disque en une passe."""
    url = f"{BASE_URL}/{dataset_id}/exports/parquet"
    temporaire = destination.with_suffix(destination.suffix + ".partiel")
    with urllib.request.urlopen(url, timeout=600) as reponse:
        temporaire.write_bytes(reponse.read())
    # Renommage en dernier : un fichier final présent est un fichier complet.
    temporaire.replace(destination)


def ecrit_manifeste(nom: str, dataset_id: str, fichier: Path, lignes: int) -> None:
    """Trace la source, la date et le volume : exigé par la Licence Ouverte."""
    manifeste = {
        "jeu": nom,
        "dataset_id": dataset_id,
        "url_source": f"{BASE_URL}/{dataset_id}/exports/parquet",
        "page_producteur": f"https://data.economie.gouv.fr/explore/dataset/{dataset_id}",
        "producteurs": PRODUCTEURS,
        "licence": LICENCE,
        "date_telechargement": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "lignes_annoncees_par_api": lignes,
        "octets": fichier.stat().st_size,
    }
    chemin = fichier.with_suffix(".manifeste.json")
    chemin.write_text(json.dumps(manifeste, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> int:
    analyseur = argparse.ArgumentParser(description=__doc__)
    analyseur.add_argument(
        "--force",
        action="store_true",
        help="retélécharge même si le fichier existe déjà",
    )
    arguments = analyseur.parse_args()

    RAW_DIR.mkdir(parents=True, exist_ok=True)

    for nom, dataset_id in DATASETS.items():
        fichier = RAW_DIR / f"rappelconso_{nom}.parquet"

        if fichier.exists() and not arguments.force:
            print(f"[=] {nom:<9} déjà présent ({fichier.name}), --force pour refaire")
            continue

        try:
            lignes = compte_lignes(dataset_id)
            print(f"[.] {nom:<9} {lignes} lignes annoncées, téléchargement…")
            telecharge(dataset_id, fichier)
        except (urllib.error.URLError, TimeoutError) as erreur:
            print(f"[!] {nom:<9} échec : {erreur}", file=sys.stderr)
            return 1

        ecrit_manifeste(nom, dataset_id, fichier, lignes)
        taille = fichier.stat().st_size / 1_048_576
        print(f"[+] {nom:<9} {fichier.name} ({taille:.1f} Mo) + manifeste")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
