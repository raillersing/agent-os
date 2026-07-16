# Agent OS Repository Instructions

## Mission

Build and maintain a vendor-neutral Agent OS / Agent Control Plane that remains independent of any single model provider, agent runtime, tool vendor, or UI framework.

## Documentation authority

1. Read `docs/00-governance/DOC-000-documentation-governance.md` before creating or changing controlled documents.
2. Check `docs/document-register.yaml` for identifiers, owners, status, phase, and dependencies.
3. Never silently change the meaning of an approved requirement, architecture decision, security control, or contract.
4. Significant architectural changes require an ADR.
5. New controlled documents must use the controlled-document template and unique identifiers.
6. Keep machine-readable contracts synchronized with narrative specifications.
7. Do not claim a feature is implemented without repository evidence and passing validation.

## Change control

- One branch and one pull request per coherent mission.
- Do not commit, push, merge, delete, publish, or access production systems without explicit user authorization.
- Preserve unrelated changes.
- Show the proposed plan before broad or cross-cutting modifications.
- Prefer small, reviewable diffs.

## Required validation for documentation changes

Run:

```bash
python3 scripts/validate_docs.py
```

Also validate any changed OpenAPI, AsyncAPI, JSON Schema, Mermaid, PlantUML, or Structurizr files with the project-approved tooling once those tools are configured.

## Writing standard

- Use precise, testable language.
- Distinguish facts, decisions, assumptions, proposals, and open questions.
- Give stable identifiers to requirements, controls, workflows, tests, and evidence.
- Cite external standards or vendor behavior using primary sources.
- Do not manufacture citations, implementation status, test results, or approvals.
