# Rappels de produits de consommation — état des lieux

## Contexte

Commanditaire : association de défense des consommateurs (sujet 5, annexe A du
cahier des charges CDC-DIA2-UE01-2026, versionné dans
[docs/cahier-des-charges.pdf](docs/cahier-des-charges.pdf)).

Besoin exprimé : « Nous voulons publier un état des lieux des rappels de
produits : quelles familles de produits, quels risques, quelles marques
reviennent le plus, et si la situation s'aggrave. »

## Questions analytiques

Rédigées dans [docs/questions.md](docs/questions.md), à valider par le
commanditaire. Chaque question est reliée aux colonnes qui permettent d'y
répondre (EF-01).

## Données

| | |
| --- | --- |
| Source | [data.economie.gouv.fr](https://data.economie.gouv.fr) (plateforme Opendatasoft du ministère de l'Économie) |
| Jeux | `rappelconso-v2-gtin-espaces` (une ligne par fiche de rappel) et `rappelconso-v2-gtin-trie` (une ligne par produit, avec code-barres) |
| Producteurs | DGCCRF, DGAL, DGEC, DGPR |
| Licence | Licence Ouverte Etalab 2.0 |
| Période couverte | 19/01/2018 à aujourd'hui |
| Volume | environ 19 300 fiches et 19 000 produits |
| Périmètre retenu | jeu complet, les deux fichiers |

La date exacte de téléchargement et le nombre de lignes obtenu sont écrits par
`src/download.py` dans `data/raw/*.manifeste.json`, versionnés dans le dépôt.

## Dépôt

<https://github.com/adamfogiel/projet1-adam-franck-feriel> (public, branche
`main`).

## Installation

```bash
git clone https://github.com/adamfogiel/projet1-adam-franck-feriel.git
cd projet1-adam-franck-feriel
python3.11 -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

**Python 3.11** est la version de référence du projet. Le cahier des charges
demande 3.11 ou supérieur, mais les versions figées dans `requirements.txt`
n'ont pas encore de paquets précompilés pour Python 3.14 : l'installation y
tente une compilation depuis les sources et échoue sur matplotlib. Si
`python3.11` n'est pas disponible sur votre poste, voir
[docs/decisions.md](docs/decisions.md).

## Reproduire l'analyse

1. Télécharger les données : `python src/download.py`
2. Exécuter `notebooks/01_exploration.ipynb` de bout en bout
3. Lancer le tableau de bord : `streamlit run app/dashboard.py`

## Résultats principaux

À compléter : trois à cinq constats, une phrase chacun.

## Limites

À compléter à partir de [docs/anomalies.md](docs/anomalies.md). Deux limites
sont connues dès le départ :

- Le jeu recense les rappels **publiés**, pas les défauts de produits. Une
  hausse du nombre de fiches peut traduire un renforcement des contrôles ou de
  l'obligation de déclaration autant qu'une dégradation de la sécurité des
  produits.
- Le fichier trié par code-barres exclut les produits sans GTIN. Les deux jeux
  n'ont donc pas le même périmètre et leurs totaux ne sont pas comparables tels
  quels.

## Équipe

| Membre | Rôle S47 | Rôle S50 | GitHub |
| --- | --- | --- | --- |
| Adam | Chef de projet, restitution | Chef de projet, dépôt | @adamfogiel |
| Franck | Données | Restitution | à compléter |
| Feriel | Dépôt | Données | à compléter |

Le détail de la répartition est dans [docs/decisions.md](docs/decisions.md).
