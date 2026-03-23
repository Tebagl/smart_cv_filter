# Path Management in Smart CV Filter

## Overview

In version X.X, significant improvements were made to the path management system to ensure better stability, persistence, and predictability of file locations across different execution environments.

## Key Changes

### Database Path
- Previously: Database was created in a temporary or relative location
- Now: Database is created in a `data` directory next to the executable
- Benefits:
  - Consistent database location
  - Persistence across application restarts
  - Works with PyInstaller bundled applications

### Output Directories
- Previously: Output directories were relative to the source code location
- Now: Output directories are created next to the executable
- Directories:
  - `output/RECLUTADOS`: Recruited CVs
  - `output/DISCARDED`: Discarded CVs

## Technical Implementation

### Path Determination
```python
try:
    # For PyInstaller bundled applications
    BASE_DIR = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).resolve().parent
except Exception:
    BASE_DIR = Path(__file__).resolve().parent
```

### Database Initialization
```python
data_dir = Path(base_path) / 'data'
os.makedirs(data_dir, exist_ok=True)
db_path = data_dir / 'smart_cv.db'
```

## Compatibility
- Works with both development and bundled (PyInstaller) environments
- Ensures table creation on first run
- Provides consistent file locations across different execution contexts

## Troubleshooting
- If you encounter permission issues, ensure the application has write permissions in the executable directory
- Check that the `data` and `output` directories are not blocked by system security settings