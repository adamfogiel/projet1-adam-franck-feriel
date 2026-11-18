# Questions analytiques

Statut : **brouillon, à valider par le commanditaire** (jalon J1, exigence EF-01).

Le besoin exprimé — « quelles familles de produits, quels risques, quelles
marques reviennent le plus, et si la situation s'aggrave » — est reformulé
ci-dessous en questions tranchables par un calcul sur les colonnes disponibles.

Chaque question nomme les colonnes qui permettent d'y répondre. Une question
sans colonne en face n'est pas traitable et doit être retirée ou reformulée.

---

## Q1. Quelles familles de produits concentrent les rappels, et cette répartition a-t-elle changé depuis 2018 ?

- **Colonnes** : `categorie_produit`, `sous_categorie_produit`, `date_publication`
- **Calcul** : nombre de fiches par catégorie et par année ; part de chaque
  catégorie dans le total annuel.
- **Couvre** : EF-04 (agrégation temporelle, agrégation par catégorie, et le
  croisement des deux).

## Q2. Quels motifs et quels risques dominent, et diffèrent-ils selon la famille de produits ?

- **Colonnes** : `motif_rappel`, `risques_encourus`, `categorie_produit`
- **Calcul** : fréquence des motifs après normalisation du texte libre ;
  croisement motif × catégorie.
- **Piège** : `motif_rappel` et `risques_encourus` sont en texte libre et
  non normalisés. La normalisation retenue doit être documentée dans
  `docs/decisions.md`, sinon les comptages ne veulent rien dire.

## Q3. Le nombre de rappels augmente-t-il, et à quel rythme ?

- **Colonnes** : `date_publication`, `numero_fiche`
- **Calcul** : nombre de fiches distinctes par mois ; comparaison d'une année
  sur l'autre.
- **Limite à énoncer** : on mesure les rappels **publiés**, pas les défauts
  réels. Une hausse peut venir d'un renforcement des contrôles. Cette limite
  doit figurer dans le tableau de bord (TB-05), pas seulement ici.

## Q4. Quelles marques et quels distributeurs reviennent le plus souvent ?

- **Colonnes** : `marque_produit`, `distributeurs`, `numero_fiche`
- **Calcul** : nombre de fiches distinctes par marque, après normalisation.
- **Piège** : 1 743 fiches (9 %) portent la valeur `sans marque`, qui est la
  valeur la plus fréquente de la colonne. Traitée comme une marque, elle arrive
  en tête du classement (ANO-04). La source est déjà en minuscules : les
  variantes restantes sont orthographiques et demandent un regroupement manuel
  sur les marques les plus fréquentes.
- **Déontologie** : un classement de marques nomme des entreprises réelles. Il
  est présenté avec son dénominateur (une marque très présente en rayon a
  mécaniquement plus de rappels) et avec ses limites, jamais comme un palmarès
  de la dangerosité.

## Q5. Combien de temps un produit reste-t-il commercialisé avant son rappel ?

- **Colonnes** : `date_debut_commercialisation`, `date_publication`
- **Calcul** : écart en jours, distribution par catégorie.
- **Traitable** : vérifié le 18/11, `date_debut_commercialisation` est remplie
  à 78,3 % et `date_fin_commercialisation` à 76,9 %. La question est conservée.
- **Piège restant** : les fiches sans ces dates ne sont probablement pas
  réparties au hasard entre catégories. Mesurer le taux de remplissage **par
  catégorie** avant de comparer des durées entre catégories.

---

## Hypothèses à tester (EF-05)

À formuler **avant** tout calcul, puis confirmer ou infirmer par écrit.

- **H1** : à écrire avant le 20/11.
- **H2** : à écrire avant le 20/11.
