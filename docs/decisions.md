# Journal des décisions

Toute décision qui engage le périmètre, la méthode ou l'organisation est notée
ici avec sa date et sa justification (section 11 du cahier des charges). Non
tracée, une décision n'existe pas pour le jury.

---

## 2026-11-18 — Sujet retenu

Sujet 5, sécurité des produits de consommation (RappelConso V2). Équipe de
trois : Adam, Franck, Feriel.

## 2026-11-18 — Répartition des rôles et rotation

| Membre | S47 (16-20/11) | S50 (07-11/12) |
| --- | --- | --- |
| Adam | Chef de projet + restitution | Chef de projet + dépôt |
| Franck | Données | Restitution |
| Feriel | Dépôt | Données |

Le chef de projet est fixe sur tout le projet et cumule un second rôle, l'équipe
comptant trois membres. Les trois autres rôles tournent à chaque semaine école ;
il ne reste qu'une rotation, appliquée en S50.

## 2026-11-18 — Deux jeux téléchargés, pas un

Les deux variantes de RappelConso V2 sont récupérées :
`rappelconso-v2-gtin-espaces` (une ligne par fiche) et
`rappelconso-v2-gtin-trie` (une ligne par produit, avec code-barres).

Justification : la jointure exigée par EF-06 se fait entre ces deux fichiers,
sur `numero_fiche` et `numero_version`. Télécharger un seul fichier rendrait
l'exigence intraitable.

## 2026-11-18 — Écart au jalon J3 assumé

Le jalon J3 attend un tableau de bord en version bêta au 20/11. Le projet
démarre le 18/11. Le tag v0.3 de vendredi contiendra : données chargées,
nettoyage v1, questions analytiques écrites, premiers indicateurs, squelette de
tableau de bord qui se lance.

Action : signaler l'écart au responsable pédagogique et archiver la réponse
dans le dépôt. Un écart signalé se discute, un écart masqué se découvre en
recette.

## 2026-11-18 — Le fichier des fiches reste la référence pour compter les rappels

Le fichier trié par code-barres exclut 34,3 % des fiches, qui n'ont aucun
produit avec GTIN (ANO-01). Tout dénombrement de rappels se fait donc sur
`rappelconso_fiches`, jamais sur le résultat d'une jointure interne.

La question Q5 est conservée : les dates de commercialisation sont remplies à
78 % et 77 %, et non « très incomplètes » comme nous le supposions.

## 2026-11-18 — Python 3.11 comme version de référence

Le cahier des charges demande Python 3.11 ou supérieur (ET-01). Nous figeons
3.11 pour toute l'équipe.

Justification : les versions figées dans `requirements.txt` (matplotlib 3.9.2,
pandas 2.2.3, pyarrow 18.1.0) n'ont pas de paquets précompilés pour Python
3.14. L'installation y bascule sur une compilation depuis les sources, qui
échoue. Constaté le 18/11 sur un poste en 3.14.8.

Deux sorties possibles si un membre n'a que 3.14 : installer 3.11, ou relever
les versions du `requirements.txt`. La seconde impose de revalider que tout le
monde obtient les mêmes résultats — à ne faire que si nécessaire, et à tracer
ici.

## 2026-11-19 — Dépôt public créé et `main` protégée

Dépôt : <https://github.com/adamfogiel/projet1-adam-franck-feriel>, public
(GIT-01).

La branche `main` exige une pull request avec une approbation d'un autre membre,
refuse les poussées forcées et la suppression de branche, et impose la
résolution des commentaires avant fusion. La restriction s'applique aux
administrateurs : une tentative de poussée directe par le propriétaire a été
rejetée (`protected branch hook declined`).

Conséquence assumée : plus aucun changement ne peut entrer dans `main` avant que
Franck et Feriel soient collaborateurs, puisqu'une PR ne s'auto-approuve pas.
C'est le prix de la preuve demandée par GIT-02 et GIT-03.

Le circuit est écrit dans [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## À trancher cette semaine

- [ ] **Schéma de `data/processed/rappels.parquet`** — Franck, avant toute
      ligne de nettoyage. Liste des colonnes conservées et leurs types, à
      recopier ici. C'est le contrat sur lequel Feriel et Adam travaillent.
- [ ] **Type de jointure entre les deux fichiers** — voir ANO-01 et ANO-02.
      Une jointure interne perd 34 % des rappels, une jointure gauche multiplie
      les lignes. Le choix se fait indicateur par indicateur et s'écrit ici.
- [ ] **Sort de la valeur `sans marque`** — 9 % des fiches, voir ANO-04. À
      trancher avant tout classement de marques (Q4).
- [ ] **Méthode de regroupement de `marque_produit`** — voir Q4. La source
      étant déjà en minuscules, il s'agit d'un regroupement manuel sur les
      marques les plus fréquentes, pas d'une normalisation automatique.
- [ ] **Identifiants GitHub des trois membres** à reporter dans le README.
