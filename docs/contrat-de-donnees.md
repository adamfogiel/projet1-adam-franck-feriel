# Contrat de données

Décision du chef de projet, 27/11/2026. Ce fichier fige l'interface entre les
trois lots pour que chacun avance sans attendre les autres.

Il répond au point resté ouvert depuis le 18/11 : « schéma de
`data/processed/rappels.parquet`, avant toute ligne de nettoyage ».

---

## 1. La table nettoyée

`src/cleaning.py` (lot A, Franck) produit `data/processed/rappels.parquet`.
**Une ligne par fiche de rappel**, jamais par produit : le dénombrement des
rappels se fait sur ce fichier.

| Colonne | Type | Règle |
| --- | --- | --- |
| `numero_fiche` | `string` | clé unique, vérifiée à l'écriture |
| `date_publication` | `datetime64[ns]` | sans fuseau ; la source est en UTC, on retire le fuseau après conversion |
| `annee` | `int16` | dérivée de `date_publication` |
| `mois` | `string` | format `AAAA-MM`, pour trier sans ambiguïté |
| `categorie_produit` | `category` | 10 modalités, inchangées |
| `sous_categorie_produit` | `category` | 57 modalités, inchangées |
| `marque_produit` | `string` | `sans marque`, `/` et la chaîne vide deviennent nuls |
| `risques` | `list<string>` | `risques_encourus` dépilée sur `\|`, valeurs mises à plat |
| `nature_juridique_rappel` | `category` | 2 modalités, nulle hors périmètre métier |
| `rembourse` / `echange` / `repare` | `boolean` | lus dans `modalites_de_compensation`, nuls hors périmètre métier |
| `a_rapporter` / `a_detruire` / `a_contacter` | `boolean` | lus dans `conduites_a_tenir_par_le_consommateur`, mêmes nuls |
| `zone_nationale` | `boolean` | vrai si `zone_geographique_de_vente` vaut `france entière` |
| `zones` | `list<string>` | zones locales dépilées sur `\|`, vide si nationale |
| `date_fin_commercialisation` | `datetime64[ns]` | nulle si absente |
| `delai_rappel_jours` | `Int32` | `date_publication − date_fin_commercialisation` ; nul si négatif ou supérieur à 3 650 |
| `fiche_complete` | `boolean` | faux pour les 2 192 fiches en `numero_version = 0`, dont tous les champs métier sont vides |

### Deux règles qui ne se négocient pas

**Le périmètre temporel commence en 2021.** Les 238 fiches de 2018-2020 sont
écartées : RappelConso n'a ouvert qu'en avril 2021, et janvier 2021 ne compte
que 8 fiches. Elles sont retirées dans `cleaning.py`, pas dans le dashboard,
pour que le notebook et le tableau de bord voient le même périmètre.

**`fiche_complete` conditionne cinq colonnes.** Tout indicateur qui touche la
nature juridique, la compensation, les conduites ou la zone filtre d'abord sur
`fiche_complete`, et affiche son dénominateur (17 071 et non 19 025).

## 2. Les indicateurs

`src/indicators.py` (lot B, Feriel) expose les fonctions ci-dessous. Le tableau
de bord n'appelle que celles-là et ne calcule rien lui-même (QC-03).

| Fonction | Rend | Colonnes attendues |
| --- | --- | --- |
| `charge_rappels()` | la table nettoyée | le schéma ci-dessus |
| `indicateurs_cles(df)` | 1 ligne | `total`, `evolution_12_mois`, `part_alimentaire`, `risque_n1`, `part_risque_n1`, `part_rembourse`, `part_tardif` |
| `rappels_par_annee(df)` | 1 ligne par année | `annee`, `rappels`, `listeria`, `part_listeria` |
| `rappels_par_categorie(df)` | 1 ligne par catégorie | `categorie`, `rappels`, `part` |
| `sous_categories(df, categorie, n)` | n lignes | `sous_categorie`, `rappels` |
| `risques_dominants(df, n)` | n lignes | `risque`, `rappels`, `part` |
| `marques_recurrentes(df, n)` | n lignes | `marque`, `rappels`, `categorie_dominante`, `risque_dominant` |

Chaque fonction reçoit le DataFrame **déjà filtré** par le tableau de bord :
les filtres de période et de catégorie s'appliquent une fois, en amont
(TB-02), et ne sont pas réimplémentés dans chaque indicateur.

## 3. Ce que fait le tableau de bord en attendant

`app/dashboard.py` (lot C, Adam) est écrit contre ce contrat et se lance dès
maintenant. Tant qu'une fonction n'est pas livrée, le bloc concerné affiche le
nom de son lot au lieu de son graphique. La structure, les titres, les limites
et les filtres sont donc démontrables sans attendre.
