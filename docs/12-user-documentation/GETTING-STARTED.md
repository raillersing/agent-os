# Guide de Démarrage Rapide - Agent OS

**Version:** 0.1.0  
**Dernière mise à jour:** 2026-07-20

## Introduction

Agent OS est un système d'exploitation pour agents IA qui fournit un Control Plane vendor-neutral pour orchestrer, gérer et surveiller des agents intelligents.

## Prérequis

- Python 3.10+
- Docker (recommandé)
- Accès à une API LLM (OpenAI, Anthropic, etc.)

## Installation Rapide

### Option 1: Docker (Recommandé)

```bash
# Cloner le dépôt
git clone https://github.com/raillersing/agent-os.git
cd agent-os

# Lancer avec Docker Compose
docker-compose up -d

# Vérifier l'installation
curl http://localhost:8080/health
```

### Option 2: Installation Locale

```bash
# Cloner le dépôt
git clone https://github.com/raillersing/agent-os.git
cd agent-os

# Installer les dépendances
pip install -r requirements.txt

# Configurer l'environnement
cp .env.example .env
# Éditer .env avec vos clés API

# Lancer le serveur
python -m agent_os.server
```

## Configuration Initiale

### 1. Configurer les clés API

Éditez le fichier `.env`:

```env
# LLM Providers
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Agent OS
AGENT_OS_SECRET_KEY=votre-cle-secrete
AGENT_OS_PORT=8080
```

### 2. Créer votre premier agent

```bash
# Via l'API
curl -X POST http://localhost:8080/api/v1/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "mon-premier-agent",
    "model": "gpt-4",
    "capabilities": ["text-generation", "code-analysis"]
  }'
```

### 3. Exécuter une tâche

```bash
# Envoyer une requête à l'agent
curl -X POST http://localhost:8080/api/v1/agents/mon-premier-agent/run \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyse ce code et suggère des améliorations",
    "context": {
      "code": "def hello(): print(\"Hello World\")"
    }
  }'
```

## Concepts Clés

### Agents
Les agents sont des entités autonomes qui peuvent exécuter des tâches. Chaque agent a:
- Un **modèle** LLM sous-jacent
- Des **capacités** (outils disponibles)
- Des **politiques** de sécurité et d'autonomie

### Control Plane
Le Control Plane orchestre les agents et gère:
- Le **routing** des requêtes
- La **mémoire** partagée
- Les **politiques** de sécurité
- La **facturation** et les coûts

### Mémoire
Agent OS gère plusieurs niveaux de mémoire:
- **Court terme**: Contexte de session
- **Long terme**: Persistance entre sessions
- **Partagée**: Entre agents

## Prochaines Étapes

1. [Installation Détaillée](./guides/INSTALLATION.md)
2. [Référence API](./API-REFERENCE.md)
3. [Créer un Agent Personnalisé](./tutorials/CREATING-YOUR-FIRST-AGENT.md)
4. [Configurer la Sécurité](./guides/SECURITY-SETUP.md)

## Assistance

- Consultez la [FAQ](./FAQ.md)
- Ouvrez un [GitHub Issue](https://github.com/raillersing/agent-os/issues)
- Rejoignez la [Discord Community](https://discord.gg/agent-os)
