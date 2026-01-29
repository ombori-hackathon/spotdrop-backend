# Build Skill

Install backend dependencies.

## Usage

```
/build
```

## Commands

```bash
cd spotdrop-backend
pip install -e ".[dev]"
```

## What it does

1. Installs all production dependencies from pyproject.toml
2. Installs development dependencies (pytest, ruff, mypy)
3. Installs the package in editable mode
