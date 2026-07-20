# Agent OS - Instructions pour Claude Code

## Vue d'ensemble du projet

Agent OS est un système d'exploitation pour agents IA - un Control Plane vendor-neutral qui orchestre des agents, gère la mémoire, les outils, et les politiques de sécurité.

## Structure du projet

```
agent-os/
├── docs/                    # Documentation contrôlée
│   ├── 00-governance/       # Gestion documentaire, glossaire
│   ├── 01-product/          # Vision, scope, PRD, personas
│   ├── 02-requirements/     # Spécifications fonctionnelles
│   ├── 03-architecture/     # Architecture système, données
│   ├── 04-contracts/        # API, schémas, contrats
│   ├── 05-ai-governance/    # Autonomie, politiques IA
│   ├── 06-security/         # IAM, sandbox, menace
│   ├── 07-ux-design/        # Accessibilité, design system
│   ├── 08-delivery/         # Dev, tests, qualité
│   ├── 09-operations/       # Observabilité, déploiement
│   ├── 10-modules/          # Spécifications modules
│   ├── 11-integrations/     # Adaptateurs (Hermes, Codex)
│   ├── 12-user-documentation/ # Guides utilisateurs
│   ├── 13-assurance/        # Audit, validation
│   └── research/            # Recherche, analyse vidéo
├── schemas/                 # Schémas JSON (vide - à compléter)
├── scripts/                 # Scripts utilitaires
│   └── validate_docs.py     # Validation documentaire
└── references/              # Références externes
```

## Conventions de nommage

### Fichiers de documentation
Format: `{CATALOGUE}-{NUMéro}-{titre-kebab-case}-v{version}.md`
Exemples:
- `SCP-001-scope-and-boundaries-v0.1.0.md`
- `SEC-001-security-architecture-v0.1.0.md`

### Catalogues utilisés
- `SCP` = Scope
- `VSN` = Vision
- `PRD` = Product Requirements Document
- `PER` = Personas
- `UCD` = Use Cases
- `SRS` = Software Requirements Specification
- `NFR` = Non-Functional Requirements
- `RTM` = Requirements Traceability Matrix
- `SAD` = System Architecture Description
- `C4` = Diagrammes C4
- `DAT` = Data Architecture
- `DCT` = Data Dictionary
- `DDD` = Domain-Driven Design
- `INT` = Integration
- `MEM` = Memory
- `SEC` = Security
- `AUT` = Autonomy
- `POL` = Policy
- `CST` = Cost
- `AGC` = Agent Contract
- `API` = API Specification
- `EVT` = Event Catalog
- `MOD` = Model Profile
- `RUN` = Run Contract
- `ART` = Artifact
- `APR` = Approval
- `IAM` = Identity & Access Management
- `SAN` = Sandbox
- `THR` = Threat Model
- `A11Y` = Accessibility
- `DSN` = Design System
- `UXA` = UX Architecture
- `DEV` = Development
- `TST` = Test Strategy
- `BCP` = Business Continuity
- `DEP` = Deployment
- `OBS` = Observability
- `OPS` = Operations
- `CAP` = Capability
- `ORC` = Orchestration
- `PLG` = Plugin
- `ADP` = Adapter
- `AUD` = Audit
- `QAG` = Quality Assurance
- `VVR` = Visual Validation

## Statut des documents

Les documents doivent avoir un statut dans leur en-tête:
- `draft` → En rédaction
- `review` → En revue
- `approved` → Approuvé
- `deprecated` → Obsolète

## Commandes utiles

### Validation documentaire
```bash
python3 scripts/validate_docs.py
```

### Vérifier la structure
```bash
find docs -name "*.md" -type f | sort
```

## Règles de travail

1. **Ne pas modifier** les documents marqués `approved` sans validation
2. **Utiliser les templates** dans `docs/00-governance/templates/`
3. **Respecter le format** `{CATALOGUE}-{NUMéro}-{titre}.md`
4. **Mettre à jour** `document-register.yaml` après ajout/modification
5. **Versionner** les changements importants avec ADR

## Patterns d'implémentation

### Architecture
- Style hexagonal / ports & adapters
- Event-driven pour la communication
- Plugin-based pour l'extensibilité

### Sécurité
- Zero-trust par défaut
- Sandboxing pour l'exécution d'agents
- Audit trail complet

### IA
- Routing intelligent des requêtes
- Politiques d'autonomie configurables
- Gestion des coûts par budget

## Contacts

- Product Owner: À définir
- Tech Lead: À définir
- Security: À définir
