<#
.SYNOPSIS
    Development helper script for Organizador Automático de Arquivos
.DESCRIPTION
    Provides common development tasks without requiring make/just.
    Run with: .\dev.ps1 <command>
.EXAMPLE
    .\dev.ps1 setup
    .\dev.ps1 test
    .\dev.ps1 build-all
    .\dev.ps1 check
#>

param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet(
        'setup', 'setup-dev',
        'format', 'lint', 'typecheck', 'security', 'check',
        'test', 'test-fast',
        'build-cli', 'build-gui', 'build-all', 'build-pkg',
        'precommit', 'precommit-install',
        'clean', 'clean-all',
        'version', 'bump-patch', 'bump-minor', 'bump-major',
        'run-cli', 'run-gui', 'help'
    )]
    [string]$Command
)

$VenvPath = "venv"
$Python = "python"
$Pip = "pip"
$VenvActivate = "& '$VenvPath\Scripts\Activate.ps1'"

function Invoke-InVenv {
    param([scriptblock]$ScriptBlock)
    & "$VenvPath\Scripts\Activate.ps1"
    & $ScriptBlock
}

function Test-Venv {
    if (-not (Test-Path "$VenvPath\Scripts\python.exe")) {
        Write-Error "Virtual environment not found at '$VenvPath'. Run '.\dev.ps1 setup' first."
        exit 1
    }
}

switch ($Command) {
    'help' {
        Write-Host "Organizador - Development Commands" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Setup:" -ForegroundColor Yellow
        Write-Host "  setup         - Create venv and install all dependencies"
        Write-Host "  setup-dev     - Install dev dependencies only"
        Write-Host ""
        Write-Host "Code Quality:" -ForegroundColor Yellow
        Write-Host "  format        - Format code with Black + isort"
        Write-Host "  lint          - Run flake8 linting"
        Write-Host "  typecheck     - Run mypy type checking"
        Write-Host "  security      - Run bandit + safety security scans"
        Write-Host "  check         - Run all checks"
        Write-Host ""
        Write-Host "Testing:" -ForegroundColor Yellow
        Write-Host "  test          - Run all tests with coverage"
        Write-Host "  test-fast     - Run tests without coverage"
        Write-Host ""
        Write-Host "Building:" -ForegroundColor Yellow
        Write-Host "  build-cli     - Build CLI executable"
        Write-Host "  build-gui     - Build GUI executable"
        Write-Host "  build-all     - Build both executables"
        Write-Host "  build-pkg     - Build wheel and sdist package"
        Write-Host ""
        Write-Host "Pre-commit:" -ForegroundColor Yellow
        Write-Host "  precommit     - Run pre-commit on all files"
        Write-Host "  precommit-install - Install pre-commit hooks"
        Write-Host ""
        Write-Host "Cleanup:" -ForegroundColor Yellow
        Write-Host "  clean         - Remove build artifacts, cache"
        Write-Host "  clean-all     - Clean + remove venv"
        Write-Host ""
        Write-Host "Version:" -ForegroundColor Yellow
        Write-Host "  version       - Show current version"
        Write-Host "  bump-patch    - Bump patch version"
        Write-Host "  bump-minor    - Bump minor version"
        Write-Host "  bump-major    - Bump major version"
        Write-Host ""
        Write-Host "Run:" -ForegroundColor Yellow
        Write-Host "  run-cli       - Run CLI"
        Write-Host "  run-gui       - Run GUI"
    }

    'setup' {
        Write-Host "Creating virtual environment..." -ForegroundColor Green
        & $Python -m venv $VenvPath
        Write-Host "Installing dependencies..." -ForegroundColor Green
        Invoke-InVenv { & $Pip install --upgrade pip }
        Invoke-InVenv { & $Pip install -r requirements.txt }
        Invoke-InVenv { & $Pip install -r requirements-dev.txt }
        Write-Host "Installing pre-commit hooks..." -ForegroundColor Green
        Invoke-InVenv { pre-commit install }
        Write-Host "Setup complete!" -ForegroundColor Cyan
    }

    'setup-dev' {
        Test-Venv
        Write-Host "Updating dependencies..." -ForegroundColor Green
        Invoke-InVenv { & $Pip install --upgrade pip }
        Invoke-InVenv { & $Pip install -r requirements-dev.txt }
        Invoke-InVenv { pre-commit install }
        Write-Host "Dev dependencies updated!" -ForegroundColor Cyan
    }

    'format' {
        Test-Venv
        Write-Host "Formatting with Black..." -ForegroundColor Green
        Invoke-InVenv { black organizer.py organizer_gui.py organizador/ tests/ --line-length=100 }
        Write-Host "Sorting imports with isort..." -ForegroundColor Green
        Invoke-InVenv { isort organizer.py organizer_gui.py organizador/ tests/ --profile=black --line-length=100 }
        Write-Host "Formatting complete!" -ForegroundColor Cyan
    }

    'lint' {
        Test-Venv
        Write-Host "Linting with flake8..." -ForegroundColor Green
        Invoke-InVenv { flake8 organizer.py organizer_gui.py organizador/ tests/ --max-line-length=100 --ignore=E501,W503 }
        Write-Host "Linting complete!" -ForegroundColor Cyan
    }

    'typecheck' {
        Test-Venv
        Write-Host "Type checking with mypy..." -ForegroundColor Green
        Invoke-InVenv { mypy organizer.py organizer_gui.py organizador/ --ignore-missing-imports --strict-optional }
        Write-Host "Type checking complete!" -ForegroundColor Cyan
    }

    'security' {
        Test-Venv
        Write-Host "Security scan with Bandit..." -ForegroundColor Green
        Invoke-InVenv { bandit -r organizer.py organizer_gui.py organizador/ -ll }
        Write-Host "Dependency vulnerability check with Safety..." -ForegroundColor Green
        Invoke-InVenv { safety check }
        Write-Host "Security scans complete!" -ForegroundColor Cyan
    }

    'check' {
        .\dev.ps1 format
        .\dev.ps1 lint
        .\dev.ps1 typecheck
        .\dev.ps1 security
    }

    'test' {
        Test-Venv
        Write-Host "Running tests with coverage..." -ForegroundColor Green
        Invoke-InVenv { python -m pytest tests/ -v --tb=short --cov=organizador --cov=organizer --cov=organizer_gui --cov-report=term-missing --cov-report=html }
        Write-Host "Tests complete!" -ForegroundColor Cyan
    }

    'test-fast' {
        Test-Venv
        Write-Host "Running tests (fast)..." -ForegroundColor Green
        Invoke-InVenv { python -m pytest tests/ -v --tb=short -x }
        Write-Host "Tests complete!" -ForegroundColor Cyan
    }

    'build-cli' {
        Test-Venv
        Write-Host "Building CLI executable..." -ForegroundColor Green
        Invoke-InVenv { pyinstaller --onefile --clean --name organizer organizer.py }
        Write-Host "CLI executable in dist/organizer.exe" -ForegroundColor Cyan
    }

    'build-gui' {
        Test-Venv
        Write-Host "Building GUI executable..." -ForegroundColor Green
        Invoke-InVenv { pyinstaller --onefile --windowed --clean --name organizer_gui organizer_gui.py }
        Write-Host "GUI executable in dist/organizer_gui.exe" -ForegroundColor Cyan
    }

    'build-all' {
        .\dev.ps1 build-cli
        .\dev.ps1 build-gui
        Write-Host "Both executables built!" -ForegroundColor Cyan
    }

    'build-pkg' {
        Test-Venv
        Write-Host "Building Python package..." -ForegroundColor Green
        Invoke-InVenv { python -m build --wheel --sdist }
        Invoke-InVenv { twine check dist/* }
        Write-Host "Package built in dist/" -ForegroundColor Cyan
    }

    'precommit' {
        Test-Venv
        Write-Host "Running pre-commit on all files..." -ForegroundColor Green
        Invoke-InVenv { pre-commit run --all-files }
        Write-Host "Pre-commit complete!" -ForegroundColor Cyan
    }

    'precommit-install' {
        Test-Venv
        Write-Host "Installing pre-commit hooks..." -ForegroundColor Green
        Invoke-InVenv { pre-commit install }
        Write-Host "Pre-commit hooks installed!" -ForegroundColor Cyan
    }

    'clean' {
        Write-Host "Cleaning build artifacts..." -ForegroundColor Yellow
        @("build", "dist", ".pytest_cache", ".mypy_cache", ".ruff_cache", "htmlcov") | ForEach-Object {
            if (Test-Path $_) { Remove-Item -Recurse -Force $_; Write-Host "  Removed $_" }
        }
        @("*.spec", ".coverage", "coverage.xml", "bandit-report.json", "safety-report.json", "safety-precommit.json") | ForEach-Object {
            Get-ChildItem $_ -ErrorAction SilentlyContinue | Remove-Item -Force
        }
        Write-Host "Clean done!" -ForegroundColor Cyan
    }

    'clean-all' {
        .\dev.ps1 clean
        Write-Host "Removing virtual environment..." -ForegroundColor Yellow
        if (Test-Path $VenvPath) { Remove-Item -Recurse -Force $VenvPath; Write-Host "  Removed $VenvPath" }
        Write-Host "Full clean done!" -ForegroundColor Cyan
    }

    'version' {
        Test-Venv
        Invoke-InVenv { python -c "import organizador; print(organizador.__version__)" }
    }

    'bump-patch' {
        Test-Venv
        Invoke-InVenv {
            python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{m.group(2)}.{int(m.group(3))+1}\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"
        }
    }

    'bump-minor' {
        Test-Venv
        Invoke-InVenv {
            python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{m.group(1)}.{int(m.group(2))+1}.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"
        }
    }

    'bump-major' {
        Test-Venv
        Invoke-InVenv {
            python -c "
import re
with open('organizador/__init__.py', 'r') as f: content = f.read()
new = re.sub(r'__version__ = \"(\d+)\.(\d+)\.(\d+)\"', lambda m: f'__version__ = \"{int(m.group(1))+1}.0.0\"', content)
with open('organizador/__init__.py', 'w') as f: f.write(new)
import organizador; print(f'Bumped to {organizador.__version__}')
"
        }
    }

    'run-cli' {
        Test-Venv
        Invoke-InVenv { python organizer.py }
    }

    'run-gui' {
        Test-Venv
        Invoke-InVenv { python organizer_gui.py --gui }
    }
}