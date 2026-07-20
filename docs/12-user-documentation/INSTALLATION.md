---
document_id: UG-INSTALLATION
title: Guide d'Installation Détaillé - Agent OS
version: 0.1.0
status: draft
owner: documentation-owner
approvers:
  - product-owner
  - operations-owner
created: 2026-07-20
last_reviewed: 2026-07-20
classification: public
source_of_truth: false
related_documents:
  - DEP-001
  - OPS-001
  - SEC-001
related_adrs: []
---

# Guide d'Installation Détaillé - Agent OS

**Version:** 0.1.0
**Dernière mise à jour:** 2026-07-20

## Table des Matières

1. [Prérequis Système](#prérequis-système)
2. [Installation via Docker](#installation-via-docker)
3. [Installation Locale](#installation-locale)
4. [Configuration](#configuration)
5. [Vérification](#vérification)
6. [Dépannage](#dépannage)

---

## Prérequis Système

### Minimum

| Composant | Version | Notes |
|-----------|---------|-------|
| Python | 3.10+ | Avec pip |
| Docker | 20.10+ | Optionnel mais recommandé |
| Docker Compose | 2.0+ | Pour l'installation Docker |
| Git | 2.30+ | Pour cloner le dépôt |

### Espace Disque

- Installation Docker: ~2 GB
- Installation locale: ~500 MB
- Données: Variable (dépend de l'utilisation)

### Ports Réseau

| Port | Service | Protocole |
|------|---------|-----------|
| 8080 | API Principal | HTTP/HTTPS |
| 8081 | Métriques | HTTP |
| 5432 | PostgreSQL | TCP |
| 6379 | Redis | TCP |

---

## Installation via Docker

### Étape 1: Cloner le Dépôt

```bash
git clone https://github.com/raillersing/agent-os.git
cd agent-os
```

### Étape 2: Configurer l'Environnement

```bash
# Copier le fichier d'exemple
cp .env.example .env

# Éditer la configuration
nano .env
```

Variables d'environnement essentielles:

```env
# Sécurité
AGENT_OS_SECRET_KEY=<generer-avec-openssl-rand-hex-32>

# LLM Providers (au moins un requis)
OPENAI_API_KEY=sk-...
# ou
ANTHROPIC_API_KEY=sk-ant-...

# Base de données
POSTGRES_PASSWORD=<mot-de-passe-fort>
REDIS_PASSWORD=<mot-de-passe-fort>
```

### Étape 3: Lancer les Services

```bash
# Production
docker-compose up -d

# Développement (avec logs)
docker-compose -f docker-compose.dev.yml up
```

### Étape 4: Initialiser la Base de Données

```bash
# Appliquer les migrations
docker-compose exec api alembic upgrade head

# Créer l'utilisateur admin
docker-compose exec api python -m agent_os.cli create-admin \
  --email admin@example.com \
  --password <mot-de-passe>
```

### Étape 5: Vérifier l'Installation

```bash
# Health check
curl http://localhost:8080/health

# Réponse attendue:
# {"status": "healthy", "version": "0.1.0"}
```

---

## Installation Locale

### Étape 1: Préparer l'Environnement

```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Mettre à jour pip
pip install --upgrade pip
```

### Étape 2: Installer les Dépendances

```bash
# Dépendances principales
pip install -r requirements.txt

# Dépendances de développement (optionnel)
pip install -r requirements-dev.txt
```

### Étape 3: Installer et Configurer PostgreSQL

```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# Créer la base de données
sudo -u postgres psql -c "CREATE USER agent_os WITH PASSWORD 'votre-mot-de-passe';"
sudo -u postgres psql -c "CREATE DATABASE agent_os OWNER agent_os;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE agent_os TO agent_os;"
```

### Étape 4: Installer et Configurer Redis

```bash
# Ubuntu/Debian
sudo apt-get install redis-server
sudo systemctl start redis

# Configurer le mot de passe
sudo nano /etc/redis/redis.conf
# Ajouter: requirepass votre-mot-de-passe
```

### Étape 5: Configurer l'Application

```bash
# Créer le fichier de configuration
cp config.example.yml config.yml

# Éditer la configuration
nano config.yml
```

Exemple de configuration:

```yaml
server:
  host: 0.0.0.0
  port: 8080
  debug: false

database:
  url: postgresql://agent_os:votre-mot-de-passe@localhost:5432/agent_os
  pool_size: 20

redis:
  url: redis://:votre-mot-de-passe@localhost:6379/0

llm:
  providers:
    openai:
      api_key: ${OPENAI_API_KEY}
    anthropic:
      api_key: ${ANTHROPIC_API_KEY}

security:
  secret_key: ${AGENT_OS_SECRET_KEY}
  sandbox_enabled: true
  audit_log: true
```

### Étape 6: Lancer l'Application

```bash
# Migration de la base de données
alembic upgrade head

# Démarrer le serveur
python -m agent_os.server

# Ou en arrière-plan
nohup python -m agent_os.server > agent-os.log 2>&1 &
```

---

## Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|--------|
| `AGENT_OS_SECRET_KEY` | Clé secrète pour les sessions | *Requis* |
| `AGENT_OS_PORT` | Port du serveur | `8080` |
| `AGENT_OS_HOST` | Hôte du serveur | `0.0.0.0` |
| `DATABASE_URL` | URL PostgreSQL | `postgresql://localhost/agent_os` |
| `REDIS_URL` | URL Redis | `redis://localhost:6379/0` |
| `OPENAI_API_KEY` | Clé API OpenAI | *Optionnel* |
| `ANTHROPIC_API_KEY` | Clé API Anthropic | *Optionnel* |

### Fichier de Configuration

Le fichier `config.yml` permet une configuration avancée. Voir [docs/09-operations/DEP-001-deployment-architecture-v0.1.0.md](../09-operations/DEP-001-deployment-architecture-and-environment-strategy-v0.1.0.md) pour les détails.

---

## Vérification

### Tests d'Intégrité

```bash
# Vérifier l'installation
python -m agent_os.cli doctor

# Résultat attendu:
# ✓ Python 3.10.12
# ✓ PostgreSQL connecté
# ✓ Redis connecté
# ✓ Clés API configurées
# ✓ Serveur démarré
```

### Tests Unitaires

```bash
# Lancer tous les tests
pytest

# Tests avec couverture
pytest --cov=agent_os --cov-report=html
```

### Health Check API

```bash
# Endpoint principal
curl http://localhost:8080/health

# Métriques
curl http://localhost:8081/metrics
```

---

## Dépannage

### Problème: "Connection refused" sur PostgreSQL

```bash
# Vérifier le statut
sudo systemctl status postgresql

# Redémarrer
sudo systemctl restart postgresql

# Vérifier les logs
sudo journalctl -u postgresql
```

### Problème: "Connection refused" sur Redis

```bash
# Vérifier le statut
sudo systemctl status redis-server

# Redémarrer
sudo systemctl restart redis-server

# Tester la connexion
redis-cli ping
```

### Problème: "Invalid API key"

1. Vérifiez que les clés API sont correctes dans `.env`
2. Vérifiez qu'elles n'ont pas expiré
3. Vérifiez les quotas de votre fournisseur

### Problème: "Port already in use"

```bash
# Trouver le processus
lsof -i :8080

# Tuer le processus
kill -9 <PID>
```

### Logs

```bash
# Logs Docker
docker-compose logs -f api

# Logs locaux
tail -f agent-os.log

# Logs avec plus de détail
LOG_LEVEL=DEBUG python -m agent_os.server
```

---

## Prochaines Étapes

- [Guide de Démarrage Rapide](./GETTING-STARTED.md)
- [Référence API](./API-REFERENCE.md)
- [Configuration Avancée](./guides/ADVANCED-CONFIGURATION.md)
- [Sécurité en Production](./guides/SECURITY-SETUP.md)
