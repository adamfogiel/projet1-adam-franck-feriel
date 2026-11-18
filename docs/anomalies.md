# Journal des anomalies

Responsable : Franck (S47), Feriel (S50).

Règle : **aucune ligne n'est supprimée ou corrigée sans trace écrite ici.** Une
anomalie documentée et non traitée est acceptée en recette si son impact est
énoncé ; une anomalie connue mais tue est un motif de refus du livrable.

Ce journal se remplit au fil de l'eau, pas à la fin : les raisons d'une décision
de nettoyage sont oubliées en trois jours.

Les chiffres ci-dessous ont été mesurés sur le téléchargement du **18/11/2026**
(19 263 fiches, 19 021 produits). Ils sont à recalculer à chaque nouveau
téléchargement, la source étant mise à jour quotidiennement.

Modèle à recopier pour chaque entrée :

```
## ANO-00 — titre court

- **Colonnes concernées** : nom exact dans la source
- **Description** : ce qui est observé, avec un exemple de valeur
- **Ampleur** : nombre de lignes et part du total concernée
- **Cause probable** : erreur de saisie, changement de nomenclature,
  secret statistique, doublon structurel, etc.
- **Traitement retenu** : conservé / corrigé / imputé / exclu / signalé,
  avec la justification
- **Impact sur l'analyse** : les indicateurs ou conclusions affectés
```

---

## ANO-01 — Un tiers des fiches n'a aucun produit dans le fichier trié

- **Colonnes concernées** : `numero_fiche`, `numero_version`, `gtin`
- **Description** : la jointure entre les deux fichiers sur
  `numero_fiche` + `numero_version` donne 12 664 clés communes, **6 599 fiches
  sans aucun produit en face**, et zéro produit orphelin. Le fichier trié
  exclut les produits sans code-barres, et ces 6 599 fiches n'en ont aucun.
- **Ampleur** : 6 599 fiches sur 19 263, soit **34,3 %**.
- **Cause probable** : choix du producteur, documenté sur la page du jeu. Les
  rappels d'automobiles, par exemple, n'ont pas de GTIN.
- **Traitement retenu** : à décider. Une jointure interne ferait disparaître un
  tiers des rappels sans que personne ne s'en aperçoive.
- **Impact sur l'analyse** : **majeur**. Tout comptage fait après une jointure
  interne sous-estime les rappels d'un tiers, et pas uniformément : les
  catégories sans code-barres disparaissent plus que les autres. Le fichier des
  fiches doit rester la référence pour tout dénombrement de rappels.

## ANO-02 — Relation un-à-plusieurs entre fiches et produits

- **Colonnes concernées** : `numero_fiche`, `numero_version`, `gtin`
- **Description** : le fichier trié compte 19 021 lignes pour 12 664 couples
  fiche + version. Une fiche porte en moyenne 1,5 produit, jusqu'à **88** pour
  la plus fournie.
- **Ampleur** : 12 664 clés, médiane de 1 produit par fiche, maximum 88.
- **Cause probable** : structure normale des données, un rappel pouvant viser
  plusieurs références.
- **Traitement retenu** : à décider selon l'unité de compte de chaque
  indicateur, et à écrire pour chacun.
- **Impact sur l'analyse** : une jointure naïve multiplie les lignes et gonfle
  tout comptage. Compter des **fiches distinctes**, jamais des lignes jointes.

## ANO-03 — Champs multivalués, séparateurs différents d'un fichier à l'autre

- **Colonnes concernées** : `identification_produits`,
  `conduites_a_tenir_par_le_consommateur`, `modeles_ou_references`
- **Description** : plusieurs valeurs sont empilées dans une seule cellule. Le
  séparateur change selon la colonne **et selon le fichier** :
  - `identification_produits` : virgule dans le fichier des fiches, `$` dans le
    fichier trié ; dans les deux, `|` sépare les groupes de produits.
  - `conduites_a_tenir_par_le_consommateur` : `|`, sur 15 284 lignes (79,3 %).
  - `modeles_ou_references` : `¤`, sur 2 840 lignes (14,7 %).
- **Ampleur** : 17 107 lignes de `identification_produits` contiennent une
  virgule, 5 211 un `|`.
- **Cause probable** : export à plat d'une structure imbriquée, avec un
  séparateur choisi par fichier.
- **Traitement retenu** : à décider colonne par colonne.
- **Impact sur l'analyse** : tout comptage sur ces colonnes avant éclatement
  est faux. La virgule étant aussi un caractère courant dans le texte, un
  découpage naïf de `identification_produits` dans le fichier des fiches
  produira des valeurs parasites : le fichier trié est plus sûr pour cette
  colonne.

## ANO-04 — « sans marque » est une valeur manquante déguisée

- **Colonnes concernées** : `marque_produit`
- **Description** : 1 743 fiches portent la valeur littérale `sans marque`.
  C'est la valeur la plus fréquente de la colonne, devant toute marque réelle.
- **Ampleur** : 1 743 fiches sur 19 263, soit **9,0 %**.
- **Cause probable** : produits vendus en vrac ou non marqués, saisis avec une
  valeur conventionnelle plutôt qu'un vide.
- **Traitement retenu** : à décider. Traitée comme une marque, elle arriverait
  en tête de tout classement.
- **Impact sur l'analyse** : fausse directement la question Q4. Son sort doit
  être tranché avant tout classement de marques.

## ANO-05 — Nom de colonne fautif dans la source

- **Colonnes concernées** : `date_date_fin_commercialisation`
- **Description** : la colonne porte « date » deux fois. Le nom est bien celui
  de la source, ce n'est pas une erreur de chargement.
- **Ampleur** : la colonne entière, dans les deux fichiers.
- **Cause probable** : erreur de saisie du producteur.
- **Traitement retenu** : conservé tel quel au chargement, renommé en
  `date_fin_commercialisation` au nettoyage. Le renommage est tracé ici pour
  que le lien avec la source reste lisible.
- **Impact sur l'analyse** : aucun, hors confusion de lecture.

## ANO-06 — Sept colonnes vides à plus de 60 %

- **Colonnes concernées** : `lien_vers_la_liste_des_produits` (84,1 % vides),
  `lien_vers_la_liste_des_distributeurs` (82,1 %),
  `informations_complementaires_publiques` (80,7 %),
  `description_complementaire_risque` (74,9 %), `marque_salubrite` (68,9 %),
  `informations_complementaires` (65,0 %), `preconisations_sanitaires` (62,6 %)
- **Description** : champs facultatifs de la fiche de rappel, rarement remplis.
- **Ampleur** : voir ci-dessus.
- **Cause probable** : champs optionnels côté producteur.
- **Traitement retenu** : écartées de l'analyse. Aucune ne porte une question
  analytique retenue.
- **Impact sur l'analyse** : aucun, sous réserve qu'aucune question ne s'y
  rattache plus tard.

---

## Deux pièges annoncés qui ne se vérifient pas sur ce jeu

Le cahier des charges annonce en annexe A des pièges attendus pour le sujet 5.
Deux d'entre eux ont été cherchés et **non trouvés** sur le téléchargement du
18/11. Le vérifier était nécessaire ; le consigner évite de refaire la
recherche, et de décrire en soutenance un nettoyage qui n'a pas eu lieu.

- **« Une fiche répétée sur plusieurs lignes »** : `numero_fiche` compte 19 263
  valeurs distinctes pour 19 263 lignes, et zéro ligne strictement dupliquée.
  Dans le fichier des fiches, une fiche occupe exactement une ligne. La
  répétition existe en revanche dans le fichier trié, où elle est structurelle
  (voir ANO-02).
- **« Formats de date modifiés par le producteur en juillet 2024 »** : les
  19 263 valeurs de `date_publication` sont interprétées sans erreur, sur toute
  la période 19/01/2018 → 18/11/2026. Le contrôle reste à refaire sur les deux
  colonnes de dates de commercialisation avant de conclure.

## À ouvrir ensuite

- Variantes d'écriture des marques. La source est déjà en minuscules : passer
  en minuscules et rogner les espaces ne change rien (6 505 marques distinctes
  avant comme après). Les variantes sont donc orthographiques, pas typographiques,
  et demandent un regroupement manuel sur les marques les plus fréquentes.
- 102 valeurs de `marque_produit` contiennent un séparateur (`|`, `,`, `;`) :
  plusieurs marques dans une seule cellule.
- Contrôle des dates de commercialisation postérieures à la date de publication,
  qui seraient aberrantes.
