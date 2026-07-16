# Agent OS Documentation Starter

Version: 0.1.0
Status: Initial controlled baseline

This package initializes the documentation system for a vendor-neutral Agent OS / Agent Control Plane.

## Included

- Documentation governance and source-of-truth policy (`DOC-000`)
- Starter glossary (`GLO-001`)
- Versioned document register (`docs/document-register.yaml`)
- Controlled-document and ADR templates
- Initial Product Vision and Charter skeleton (`VSN-001`)
- Repository-level `AGENTS.md` instructions for coding agents
- Reusable Codex documentation skill
- Documentation validation script
- Codex bootstrap prompt for local use

## Recommended installation

Create a dedicated repository, for example:

```bash
mkdir -p /home/raillersing/projects/agent-os
cd /home/raillersing/projects/agent-os
git init
```

Copy the contents of this starter package into the repository root, then run:

```bash
python3 scripts/validate_docs.py
```

Do not mark product, architecture, security, or governance documents as `approved` until the project owner has reviewed them.
