# Makefile - Development tasks for Organizador
# Windows: Use with Git Bash, WSL, or 'make' from Chocolatey/Scoop
# Alternative: Use 'just' (justfile) or 'dev.ps1' (PowerShell)

.PHONY: help setup setup-dev format lint typecheck security check test test-fast build-cli build-gui build-all build-pkg precommit precommit-install clean clean-all version bump-patch bump-minor bump-major run-cli run-gui

# Default target
help:
	@echo "Organizador - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make setup         - Create venv and install all dependencies"
	@echo "  make setup-dev     - Install dev dependencies only"
	@echo ""
	@echo "Code Quality:"
	@echo "  make format        - Format code with Black + isort"
	@echo "  make lint          - Run flake8 linting"
	@echo "  make typecheck     - Run mypy type checking"
	@echo "  make security      - Run bandit + safety security scans"
	@echo "  make check         - Run all checks"
	@echo ""
	@echo "Testing:"
	@echo "  make test          - Run all tests with coverage"
	@echo "  make test-fast     - Run tests without coverage"
	@echo ""
	@echo "Building:"
	@echo "  make build-cli     - Build CLI executable"
	@echo "  make build-gui     - Build GUI executable"
	@echo "  make build-all     - Build both executables"
	@echo "  make build-pkg     - Build wheel and sdist package"
	@echo ""
	@echo "Pre-commit:"
	@echo "  make precommit     - Run pre-commit on all files"
	@echo "  make precommit-install - Install pre-commit hooks"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean         - Remove build artifacts, cache"
	@echo "  make clean-all     - Clean + remove venv"
	@echo ""
	@echo "Version:"
	@echo "  make version       - Show current version"
	@echo "  make bump-patch    - Bump patch version"
	@echo "  make bump-minor    - Bump minor version"
	@echo "  make bump-major    - Bump major version"
	@echo ""
	@echo "Run:"
	@echo "  make run-cli       - Run CLI"
	@echo "  make run-gui       - Run GUI"

# Variables
PYTHON := python
PIP := pip
VENV := venv
VENV_ACTIVATE := source $(VENV)/bin/activate

# Setup
setup:
	@echo "Creating virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@echo "Installing dependencies..."
	$(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	$(VENV_ACTIVATE) && $(PIP) install -r requirements.txt
	$(VENV_ACTIVATE) && $(PIP) install -r requirements-dev.txt
	@echo "Installing pre-commit hooks..."
	$(VENV_ACTIVATE) && pre-commit install
	@echo "Setup complete!"

setup-dev:
	$(VENV_ACTIVATE) && $(PIP) install --upgrade pip
	$(VENV_ACTIVATE) && $(PIP) install -r requirements-dev.txt
	$(VENV_ACTIVATE) && pre-commit install

# Code Quality
format:
	$(VENV_ACTIVATE) && black organizer.py organizer_gui.py organizador/ tests/ --line-length=100
	$(VENV_ACTIVATE) && isort organizer.py organizer_gui.py organizador/ tests/ --profile=black --line-length=100

lint:
	$(VENV_ACTIVATE) && flake8 organizer.py organizer_gui.py organizador/ tests/ --max-line-length=100 --ignore=E501,W503

typecheck:
	$(VENV_ACTIVATE) && mypy organizer.py organizer_gui.py organizador/ --ignore-missing-imports --strict-optional

security:
	$(VENV_ACTIVATE) && bandit -r organizer.py organizer_gui.py organizador/ -ll
	$(VENV_ACTIVATE) && safety check

check: format lint typecheck security

# Testing
test:
	$(VENV_ACTIVATE) && python -m pytest tests/ -v --tb=short --cov=organizador --cov=organizer --cov=organizer_gui --cov-report=term-missing --cov-report=html

test-fast:
	$(VENV_ACTIVATE) && python -m pytest tests/ -v --tb=short -x

# Building
build-cli:
	$(VENV_ACTIVATE) && pyinstaller --onefile --clean --name organizer organizer.py

build-gui:
	$(VENV_ACTIVATE) && pyinstaller --onefile --windowed --clean --name organizer_gui organizer_gui.py

build-all: build-cli build-gui
	@echo "Executables in dist/"

build-pkg:
	$(VENV_ACTIVATE) && python -m build --wheel --sdist
	$(VENV_ACTIVATE) && twine check dist/*

# Pre-commit
precommit:
	$(VENV_ACTIVATE) && pre-commit run --all-files

precommit-install:
	$(VENV_ACTIVATE) && pre-commit install

# Cleanup
clean:
	@echo "Cleaning build artifacts..."
	rm -rf build dist *.spec .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage coverage.xml

clean-all: clean
	@echo "Removing virtual environment..."
	rm -rf $(VENV)
	@echo "Full clean done."

# Version Management
version:
	$(VENV_ACTIVATE) && python -c "import organizador; print(organizador.__version__)"

bump-patch:
	$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{m.group(2)}.{int(m.group(3))+1}\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

bump-minor:
	$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{int(m.group(2))+1}.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

bump-major:
	$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{int(m.group(1))+1}.0.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

# Run
run-cli:
	$(VENV_ACTIVATE) && python organizer.py

run-gui:
	$(VENV_ACTIVATE) && python organizer_gui.py --gui