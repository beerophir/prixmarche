# PrixMarché

Application Django de suivi des prix des produits vivriers sur les marchés.

Projet du cours de Programmation Web en Python — ISSEA, Analystes Statisticiens
3e année, année académique 2026-2027. Enseignant : Dr. Adamou Hamza.

## Fonctionnalités

- Référentiels marchés, produits et enquêteurs : liste, création, modification,
  suppression avec confirmation.
- Affectation des enquêteurs aux marchés, avec date de début et interdiction
  des doublons.
- Saisie, consultation, correction et suppression des relevés de prix.
- Tableau de bord des effectifs sur la page d'accueil.
- Interface d'administration Django pour la saisie interne.

## Modèle de données

Cinq tables, traduites du MLD du devoir :

| Table | Clé primaire | Particularité |
|---|---|---|
| `Marche` | `code_marche` (texte) | — |
| `Produit` | `code_produit` (texte) | unité : tas, régime, kilogramme |
| `Enqueteur` | `matricule` (texte) | téléphone stocké en texte |
| `Affectation` | identifiant technique | association n–n, porte `date_debut`, unicité (enquêteur, marché) |
| `Releve` | `num_releve` (auto) | trois clés étrangères : produit, marché, enquêteur |

Toutes les clés étrangères utilisent `on_delete=PROTECT` : une référence utilisée
ne peut pas être supprimée.

## Contrôles métier

Appliqués côté serveur dans `prix/forms.py` :

- la date d'un relevé ne peut pas être future ;
- le prix doit être strictement positif ;
- un enquêteur ne peut saisir un relevé que sur un marché où il est affecté ;
- un enquêteur ne peut pas être affecté deux fois au même marché
  (`UniqueConstraint` au niveau de la base).

## Installation

Prérequis : Python 3.12 ou plus récent, Git.

```bash
git clone <url-du-depot>
cd prixmarche

python -m venv .venv
.venv\Scripts\activate          # Windows
source .venv/bin/activate       # Linux / macOS

pip install -r requirements.txt
```

Créer un fichier `.env` à la racine, sur le modèle de `.env.example` :

```
DJANGO_SECRET_KEY=une-cle-aleatoire-longue
DJANGO_DEBUG=1
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
```

Pour produire une clé :

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Préparer la base et lancer le site :

```bash
python manage.py migrate
python manage.py loaddata donnees_initiales.json
python manage.py createsuperuser
python manage.py runserver
```

Le site est alors accessible sur http://127.0.0.1:8000/ et l'administration
sur http://127.0.0.1:8000/admin/.

## Jeu de données

`donnees_initiales.json` contient 3 marchés, 4 produits, 2 enquêteurs,
3 affectations et 10 relevés hebdomadaires. La base `db.sqlite3` n'est
volontairement pas versionnée.

## Déploiement

La base reste SQLite, conformément à l'énoncé. En production :

- `DJANGO_DEBUG=0` et `DJANGO_ALLOWED_HOSTS` limité au domaine utilisé ;
- `python manage.py collectstatic` puis service du dossier `staticfiles/` ;
- Gunicorn exécute l'application WSGI (`config.wsgi:application`) ;
- Nginx assure HTTPS, les fichiers statiques et le proxy inverse.

Le réglage `SECURE_HSTS_SECONDS` n'est volontairement pas activé : HSTS engage
le navigateur sur plusieurs mois et se révoque difficilement, ce qui est
disproportionné pour un déploiement pédagogique temporaire.

## Usage de l'IA

Conformément à la charte du cours, l'usage de l'IA est déclaré : le projet a été
construit pas à pas avec l'assistance d'un agent conversationnel, à partir de
l'énoncé du TP. Chaque fichier a été relu, exécuté et testé.