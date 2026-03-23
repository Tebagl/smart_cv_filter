# SRC Path Integrity Update

## Context

After relocating source code, tests, and data folders (`inputs`, `output`) under `src/`, a validation pass was required to ensure runtime paths, import behavior, and SDD rule consistency remained correct.

## Changes Applied

1. **Import resilience in entrypoint**
   - Updated `src/main.py` to support both execution modes:
     - `python3 src/main.py` (script mode)
     - `python3 -m src.main` (module mode)
   - Implemented dual import strategy (`from .module ...` with fallback to `from module ...`) for `extractor`, `anonymizer`, and `analyzer`.

2. **Rules reference consistency**
   - Fixed the link in `ai-specs/.cursor/rules/use-base-rules.mdc` so it correctly points to `ai-specs/specs/base-standards.mdc` from the rule file location.

## Validation Performed

- Reviewed `src/main.py`, `src/analyzer.py`, and test files:
  - `src/test_anonymizer.py`
  - `src/test_module.py`
  - `src/list_models_test.py`
- Confirmed path construction in `main.py` is relative to `src/` via `BASE_DIR`, so `src/inputs` and `src/output` remain valid.
- Attempted test and import execution with `python3`; full runtime verification is currently blocked by missing dependencies in the environment (`spacy`, `pdfplumber`, `google-generativeai`).

## Notes

- No additional code changes were required for `analyzer.py` or tests regarding `inputs/output` routes.
- To complete end-to-end runtime validation, install dependencies from `src/requirements.txt` and rerun tests.
