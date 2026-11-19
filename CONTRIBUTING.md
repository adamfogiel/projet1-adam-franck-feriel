# Circuit de contribution

La branche `main` est protégée. Personne ne pousse dessus directement, pas même
le propriétaire du dépôt : la restriction s'applique aussi aux administrateurs,
vérifié par une tentative réelle le 19/11/2026. Toute modification passe par une
pull request relue par un autre membre (GIT-02, GIT-03).

## Les quatre règles

1. **Une branche par tâche**, nommée `type/sujet-court` en minuscules avec des
   tirets. Les types utilisés : `data` (téléchargement, nettoyage), `indic`
   (indicateurs, statistiques), `dash` (tableau de bord), `docs`
   (documentation, journaux), `fix` (correction).
   Exemples : `data/typage-des-dates`, `indic/rappels-par-mois`,
   `dash/filtre-par-categorie`.

2. **Une pull request par branche**, dont la description dit *pourquoi* le
   changement est fait, pas seulement ce qu'il contient. Si la PR répond à une
   exigence du cahier des charges, citer son code (EF-03, TB-02, etc.).

3. **Une relecture par un autre membre** avant fusion. Une PR ne s'auto-approuve
   pas : GitHub l'interdit, et c'est voulu. Le relecteur vérifie trois choses :
   le code tourne chez lui après `git pull`, `ruff check .` passe, et une
   anomalie découverte au passage est consignée dans `docs/anomalies.md`.

4. **Pas de sortie de notebook dans un commit.** Avant de commiter un `.ipynb`,
   vider les sorties (*Kernel → Restart and Clear Output*). Les sorties rendent
   les diffs illisibles et font grossir le dépôt (QC-04).

## Rotation des rôles

Le propriétaire de chaque lot est le seul à modifier ses fichiers, pour que deux
personnes ne se marchent pas dessus :

| Fichier | S47 | S50 |
| --- | --- | --- |
| `src/cleaning.py` | Franck | Feriel |
| `src/indicators.py` | Feriel | Franck |
| `app/dashboard.py` | Adam | Adam |

Un besoin de modifier le fichier d'un autre se règle par une demande dans la PR,
pas par une modification directe.

## Pourquoi cette lourdeur sur un projet de trois personnes

Le cahier des charges fait de deux choses un motif de refus : un historique où
la contribution d'un membre est absente, et un dépôt non reproductible. Le
circuit par pull request produit les deux preuves en même temps — qui a écrit
quoi, et que quelqu'un d'autre a vérifié que ça tourne ailleurs que sur le poste
de l'auteur.
