# Justfile - Command runner for development tasks
# Install: https://github.com/casey/just
# Windows: scoop install just / choco install just / winget install Casey.Just

# Variables
PYTHON := python
PIP := pip
VENV := venv
VENV_ACTIVATE := $(VENV)\Scripts\activate

# Default recipe
default: help

# Help
help:
	@echo "Organizador - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  setup         - Create venv and install all dependencies"
	@echo "  setup-dev     - Install dev dependencies only (assumes venv exists)"
	@echo ""
	@echo "Code Quality:"
	@echo "  format        - Format code with Black + isort"
	@echo "  lint          - Run flake8 linting"
	@echo "  typecheck     - Run mypy type checking"
	@echo "  security      - Run bandit + safety security scans"
	@echo "  check         - Run all checks (format, lint, typecheck, security)"
	@echo ""
	@echo "Testing:"
	@echo "  test          - Run all tests with coverage"
	@echo "  test-fast     - Run tests without coverage (faster)"
	@echo "  test-watch    - Run tests in watch mode"
	@echo ""
	@echo "Building:"
	@echo "  build-cli     - Build CLI executable with PyInstaller"
	@echo "  build-gui     - Build GUI executable with PyInstaller"
	@echo "  build-all     - Build both executables"
	@echo "  build-pkg     - Build wheel and sdist package"
	@echo ""
	@echo "Pre-commit:"
	@echo "  precommit     - Run pre-commit on all files"
	@echo "  precommit-install - Install pre-commit hooks"
	@echo ""
	@echo "Cleanup:"
	@echo "  clean         - Remove build artifacts, cache, etc."
	@echo "  clean-all     - Clean + remove venv"
	@echo ""
	@echo "Release:"
	@echo "  version       - Show current version"
	@echo "  bump-patch    - Bump patch version (x.y.Z)"
	@echo "  bump-minor    - Bump minor version (x.Y.z)"
	@echo "  bump-major    - Bump major version (X.y.z)"

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
	@echo "Setup complete! Run 'just setup-dev' to update deps later."

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

test-watch:
	$(VENV_ACTIVATE) && python -m pytest tests/ -v --tb=short --watch

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
	@if exist build rmdir /s /q build
	@if exist dist rmdir /s /q dist
	@if exist *.spec del *.spec
	@if exist .pytest_cache rmdir /s /q .pytest_cache
	@if exist .mypy_cache rmdir /s /q .mypy_cache
	@if exist .ruff_cache rmdir /s /q .ruff_cache
	@if exist htmlcov rmdir /s /q htmlcov
	@if exist .coverage del .coverage
	@if exist coverage.xml del coverage.xml
	@echo "Clean done."

clean-all: clean
	@echo "Removing virtual environment..."
	@if exist $(VENV) rmdir /s /q $(VENV)
	@echo "Full clean done."

# Version Management
version:
	@$(VENV_ACTIVATE) && python -c "import organizador; print(organizador.__version__)"

bump-patch:
	@$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{m.group(2)}.{int(m.group(3))+1}\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

bump-minor:
	@$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{int(m.group(2))+1}.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

bump-major:
	@$(VENV_ACTIVATE) && python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{int(m.group(1))+1}.0.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"

# Run directly
run-cli:
	$(VENV_ACTIVATE) && python organizer.py

run-gui:
	$(VENV_ACTIVATE) && python organizer_gui.py --gui

run-cli-help:
	$(VENV_ACTIVATE) && python organizer.py --help