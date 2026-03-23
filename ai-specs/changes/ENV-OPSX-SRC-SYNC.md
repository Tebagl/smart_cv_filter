# Environment and OPSX Source Sync

## Scope

Operational setup and spec synchronization for the `/src` migration.

## Actions Executed

1. Attempted `.venv` creation in project root with `python3 -m venv .venv`.
2. Attempted dependency installation from `src/requirements.txt`.
3. Validated OPSX command docs in `.cursor/commands/`.
4. Synchronized `ai-specs/codex.md` to enforce `/src` path rules and OPSX-first workflow.

## Findings

- The host runtime resolves Python executable to `Cursor.AppImage`, which prevents executing `.venv/bin/python` and `.venv/bin/pip` (FUSE mount error in this environment).
- `src/requirements.txt` had an invalid pin: `numpy==2.4.3` (not available for Python 3.10). Updated to `numpy==2.2.6`.

## Applied Mitigation

- Installed dependencies to a local target folder (`.deps`) using:
  - `python3 -m pip install -r src/requirements.txt --target .deps`
- Verified runtime imports successfully with:
  - `PYTHONPATH=".deps:src" python3 -c "import main; import analyzer; import extractor; import anonymizer"`

## Result

- Dependency-related import failures are resolved for project runtime when using `PYTHONPATH=".deps:src"`.
- Specification and command guidance are now aligned with `/src` and OPSX-first operations.
