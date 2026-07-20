# Contribuer à Agent OS

Merci de votre intérêt pour Agent OS ! Ce guide explique comment contribuer au projet.

## Table des Matières

1. [Code of Conduct](#code-of-conduct)
2. [Comment Contribuer](#comment-contribuer)
3. [Développement](#développement)
4. [Style Guide](#style-guide)
5. [Pull Requests](#pull-requests)
6. [Issues](#issues)

---

## Code of Conduct

En participant à ce projet, vous acceptez de respecter notre Code of Conduct:

- Respecter les autres contributeurs
- Être constructif et bienveillant
- Se concentrer sur ce qui est meilleur pour la communauté
- Respecter les décisions du projet

---

## Comment Contribuer

### Types de Contributions

- **Bug Reports**: Signaler des bugs via GitHub Issues
- **Documentation**: Améliorer la documentation
- **Code**: Corriger des bugs ou ajouter des fonctionnalités
- **Tests**: Ajouter ou améliorer les tests
- **Design**: Proposer des améliorations UI/UX

### Première Contribution

1. Cherchez les issues标签 `good-first-issue`
2. Commentez l'issue pour indiquer que vous travaillez dessus
3. Fork le dépôt
4. Créez une branche pour votre feature
5. Faites vos modifications
6. Soumettez une Pull Request

---

## Développement

### Prérequis

- Python 3.10+
- Docker & Docker Compose
- Git

### Setup de Développement

```bash
# Cloner votre fork
git clone https://github.com/VOTRE-UTILISATEUR/agent-os.git
cd agent-os

# Ajouter le remote upstream
git remote add upstream https://github.com/raillersing/agent-os.git

# Installer les dépendances de développement
pip install -r requirements-dev.txt

# Lancer l'environnement de développement
docker-compose -f docker-compose.dev.yml up
```

### Structure du Code

```
agent_os/
├── api/            # Routes API
├── core/           # Logique métier
├── models/         # Modèles de données
├── services/       # Services
├── utils/          # Utilitaires
└── cli/            # Interface ligne de commande
```

### Tests

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=agent_os

# Tests spécifiques
pytest tests/test_agents.py -v
```

### Linting

```bash
# Vérifier le style
flake8 agent_os/
black --check agent_os/
isort --check-only agent_os/

# Formater le code
black agent_os/
isort agent_os/
```

---

## Style Guide

### Python

- Suivre PEP 8
- Utiliser Black pour le formatage
- Utiliser isort pour l'import
- Maximum 88 caractères par ligne
- Docstrings pour toutes les fonctions publiques

### Documentation

- Markdown pour la documentation
- Max 80 caractères par ligne
- Sections avec `##` uniquement
- Code blocks avec language tag

### Git

- Messages de commit en français
- Format: `<type>: <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Exemples:
```
feat: ajouter la gestion des mémoires
fix: corriger le routage des requêtes
docs: mettre à jour le guide d'installation
```

---

## Pull Requests

### Processus

1. **Créer une branche**
   ```bash
   git checkout -b feat/ma-fonctionnalite
   ```

2. **Faire vos modifications**
   - Écrire du code propre
   - Ajouter des tests
   - Mettre à jour la documentation si nécessaire

3. **Tester**
   ```bash
   pytest
   flake8 agent_os/
   black --check agent_os/
   ```

4. **Committer**
   ```bash
   git add .
   git commit -m "feat: ajouter ma fonctionnalite"
   ```

5. **Push**
   ```bash
   git push origin feat/ma-fonctionnalite
   ```

6. **Créer la Pull Request**
   - Titre descriptif
   - Description des changements
   - Référence aux issues fermées
   - Screenshots si applicable

### Critères de Revue

- [ ] Code fonctionnel
- [ ] Tests passing
- [ ] Documentation mise à jour
- [ ] Pas de régression
- [ ] Respect du style guide

### Après Merge

- Supprimer la branche locale et distante
- Pull les changements upstream

---

## Issues

### Créer une Issue

Utilisez les templates GitHub:
- **Bug Report**: Pour signaler un bug
- **Feature Request**: Pour proposer une fonctionnalité
- **Documentation**: Pour signaler un problème de doc

### Informations Incluses

- Description claire du problème
- Étapes pour reproduire
- Comportement attendu vs réel
- Environnement (OS, Python, etc.)
- Screenshots si applicable

### Étiquettes

| Étiquette | Description |
|-----------|-------------|
| `bug` | Bug confirmé |
| `enhancement` | Nouvelle fonctionnalité |
| `documentation` | Amélioration de la doc |
| `good-first-issue` | Bonne première contribution |
| `help-wanted` | Besoin d'aide |
| `priority:high` | Haute priorité |

---

## Questions ?

- Ouvrez une [Discussion GitHub](https://github.com/raillersing/agent-os/discussions)
- Rejoignez la [Discord Community](https://discord.gg/agent-os)

Merci pour vos contributions ! 🎉
