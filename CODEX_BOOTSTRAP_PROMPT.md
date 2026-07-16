# Codex Bootstrap Prompt — Agent OS Documentation Repository

Use this prompt after copying the starter package into the intended local repository.

```text
Act as the Agent OS Documentation Bootstrap Executor.

Repository:
<INSERT_ABSOLUTE_REPOSITORY_PATH>

Objective:
Validate and prepare the repository documentation baseline without inventing product decisions or marking drafts as approved.

Mandatory preflight:
1. Read AGENTS.md.
2. Read docs/00-governance/DOC-000-documentation-governance.md.
3. Read docs/00-governance/GLO-001-glossary.md.
4. Read docs/document-register.yaml.
5. Inspect git status and preserve unrelated files.

Tasks:
1. Verify the starter directory structure.
2. Run `python3 scripts/validate_docs.py`.
3. Report every validation error without hiding or bypassing it.
4. Check that all existing controlled documents are registered and IDs are unique.
5. Do not create the planned documents yet.
6. Do not change product scope, architecture, security policy, or technology decisions.
7. Do not set any document to approved or implemented.
8. Produce a concise readiness report containing:
   - repository path and branch;
   - files inspected;
   - validation result;
   - detected inconsistencies;
   - recommended next document;
   - exact changed files, if any.

Rules:
- No commit, push, pull request, merge, deletion, or publication without explicit authorization.
- Do not install dependencies unless needed and explicitly approved.
- Prefer zero changes when the baseline already validates.
- Be truthful about anything that cannot be verified.
```
