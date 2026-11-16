# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [1.1.0] - 2026-11-16

### Adicionado - Qualidade Profissional & Enterprise
- 🛡️ **Política de Segurança** (`SECURITY.md`) com versões suportadas, processo de divulgação responsável, medidas implementadas (path traversal protection, input validation, symlink protection, safe history storage)
- 🤝 **Código de Conduta** (`CODE_OF_CONDUCT.md`) baseado no Contributor Covenant v2.1
- 📋 **Templates de Issue** (`.github/ISSUE_TEMPLATE/`) - Bug Report e Feature Request estruturados
- 📝 **Pull Request Template** (`.github/PULL_REQUEST_TEMPLATE.md`) com checklist de qualidade
- 👥 **CODEOWNERS** (`.github/CODEOWNERS`) para revisão automática
- 💰 **Funding** (`.github/FUNDING.yml`) para GitHub Sponsors

### Adicionado - CI/CD Avançado
- ⚙️ **Pipeline CI Completa** (`.github/workflows/ci.yml`):
  - Lint & Format (Black, isort, flake8) - Python 3.10, 3.11, 3.12
  - Type Checking (mypy) - Multi-version
  - Unit Tests com Coverage (pytest + Codecov) - Meta ≥ 80%
  - Security Scan (Bandit + Safety) - Artefatos uploadados
  - Build Windows Executables (PyInstaller) - Apenas tags/dispatch
  - Build Python Package (wheel + sdist) - Twine check
  - GitHub Release automatizado com executáveis + packages
  - Notificação de falha
- 🤖 **Dependabot** (`.github/dependabot.yml`) - Atualizações semanais (segundas 09h BRT) para pip + GitHub Actions, agrupadas por tipo (dev, build)

### Adicionado - Developer Experience
- 🔧 **Pre-commit Hooks** (`.pre-commit-config.yaml`):
  - Trailing whitespace, EOL, YAML/TOML/JSON validation
  - Merge conflict detection, large file prevention
  - Black + isort formatting
  - Flake8 + flake8-bugbear + flake8-comprehensions linting
  - MyPy type checking
  - Bandit security scanning
  - Safety dependency vulnerability check
  - Commitlint (Conventional Commits validation)
- 📦 **Commitlint Config** (`.commitlintrc.json`) - Regras estendidas + prompts em PT-BR
- ⚡ **Task Runners** multiplataforma:
  - `justfile` (cross-platform, `just` command)
  - `Makefile` (Linux/macOS/WSL/Git Bash)
  - `dev.ps1` (PowerShell nativo Windows)
- 🎨 **EditorConfig** (`.editorconfig`) - Consistência entre IDEs
- 📚 **Documentação Técnica** (`docs/`):
  - `architecture.md` - Arquitetura completa com diagramas ASCII
  - `contributing.md` - Guia técnico detalhado para contribuidores

### Melhorado - README Profissional
- 🏷️ **Badges enterprise**: CI Status, Codecov, Security Scan, Code Style, Type Check, Total Downloads, Last Commit, Open PRs, Security Policy, PRs Welcome
- 📊 **Status badges**: Repo size, language count, top language, commit activity, contributors
- 🔗 **Links expandidos**: Documentation, Discussions, Security, Funding
- 🛡️ **Seção Segurança** com resumo de proteções implementadas
- 📂 **Estrutura do projeto** atualizada com todos novos arquivos
- ⚙️ **Setup de desenvolvimento** completo com pre-commit
- ✅ **Checklist de PR** expandido

### Melhorado - Configuração do Projeto
- 📦 **pyproject.toml** expandido:
  - URLs adicionais: Documentation, Discussions, Security
  - Keywords expandidas
  - Tool configs: Bandit, Safety, Ruff (comentado)
  - Coverage: source explícito, parallel, show_missing
  - MyPy: namespace_packages, explicit_package_bases
- 📋 **requirements-dev.txt** atualizado com versões pinadas:
  - black≥24.4.0, flake8≥7.1.0, flake8-bugbear, flake8-comprehensions
  - mypy≥1.10.0, isort≥5.13.0, pre-commit≥3.7.0
  - bandit≥1.7.8, safety≥3.0.0, build≥1.2.0, twine≥5.0.0
  - types-requests≥2.31.0

### Técnico
- Configuração Ruff adicionada (comentada) como linter moderno alternativo
- Bandit config: skip B101 (assert), B601 (subprocess sem shell)
- PyTest markers: slow, integration, gui
- Coverage omit: organizador_gui.py (GUI hard to test)
- Git ignore: .ruff_cache, .commitlintrc.json tracking

---

## [1.0.0] - 2026-11-15

### Adicionado
- 🎉 **Interface Gráfica (GUI)** completa usando Tkinter nativo
  - Seleção de pasta com botão "Procurar"
  - Checkbox para renomeação com data
  - Tabela de prévia colorida por categoria
  - Barra de progresso animada
  - Status em tempo real
  - Botão "Iniciar Organização"
  - Botão "Desfazer Organização" (aparece após sucesso)
  - Botão "Limpar Histórico"
- 🎉 **Linha de Comando (CLI)** com argparse
  - Argumento posicional para pasta (padrão: Downloads)
  - Flags `-r/--renomear`, `--dry-run`, `--gui`, `-v/--version`
  - Códigos de saída apropriados (0=sucesso, 1=erro)
- 🎉 **Sistema de Categorização** com 5 categorias
  - Documentos (.pdf, .docx, .doc, .txt, .xlsx, .pptx, .csv)
  - Imagens (.jpg, .jpeg, .png, .gif, .svg, .webp)
  - Instaladores/Executáveis (.exe, .msi, .dmg, .pkg, .deb, .rpm)
  - Compactados (.zip, .rar, .tar, .gz, .7z)
  - Outros (qualquer extensão não listada)
- 🎉 **Renomeação Inteligente**
  - Prefixo `AAAA-MM-DD_` baseado na data de criação do arquivo
  - Tratamento automático de conflitos com sufixos `_1`, `_2`...
- 🎉 **Sistema Desfazer Completo**
  - Restaura todos arquivos para pasta original
  - Remove pastas de categoria vazias
  - Trata conflitos de nome na restauração
  - Barra de progresso durante desfazimento
- 🎉 **Histórico Persistente**
  - Salva automaticamente em `.organizador_historico.json`
  - Permite desfazer mesmo após fechar/reabrir o programa
- 🎉 **Modo Prévia (Dry-run)**
  - Simula organização sem mover arquivos
  - Disponível tanto na GUI quanto CLI
- 🎉 **Executáveis Standalone**
  - `organizer.exe` (~9.5 MB) - CLI console
  - `organizer_gui.exe` (~13 MB) - GUI janela nativa
  - Gerados com PyInstaller (--onefile --windowed)
- 🎉 **CI/CD com GitHub Actions**
  - Build automático em push para main
  - Cria release com executáveis anexados
  - Testes básicos de smoke test
- 🎉 **Documentação Completa**
  - README.md com badges, screenshots ASCII, exemplos
  - LICENSE (MIT)
  - CHANGELOG.md
  - CONTRIBUTING.md
  - .gitignore completo

### Técnico
- Código 100% tipado com type hints
- Docstrings em todas as funções públicas
- Dataclasses para estruturas de dados
- Enum para categorias
- Threading para não travar GUI
- Fallback para colorama (funciona sem cores se não instalado)
- Compatível Windows/Linux/macOS (GUI apenas Windows nativamente)

---

## [Unreleased]

### Planejado
- 🌍 Internacionalização (pt-BR, en-US, es-ES)
- 🎨 Tema escuro/claro na GUI
- ⚙️ Configuração de categorias via JSON
- 📅 Integração com Agendador de Tarefas do Windows
- 🐧 Builds Linux (AppImage) e macOS (.dmg)
- 🧪 Testes unitários com pytest (cobertura ≥ 80%)
- 📦 Publicação no Chocolatey, Scoop, Winget
- 🔍 Busca recursiva em subpastas (opcional)
- 📊 Logs detalhados em arquivo
- 🔔 Notificações toast do Windows