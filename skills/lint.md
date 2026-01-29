# Lint Skill

Run linting on backend code.

## Usage

```
/lint
```

## Commands

```bash
cd spotdrop-backend
ruff check src/ tests/
ruff format --check src/ tests/
mypy src/
```

## What it does

1. Runs ruff linter for code style issues
2. Checks code formatting
3. Runs mypy for type checking

## Auto-fix

To automatically fix issues:
```bash
ruff check --fix src/ tests/
ruff format src/ tests/
```
