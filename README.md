<p align="center">
  <img src="assets/logo.png" alt="Organizador Logo" width="120" height="120">
</p>

<h1 align="center">Organizador Automático de Arquivos</h1>

<p align="center">
  <strong>Organize sua pasta Downloads (ou qualquer pasta) em segundos com uma interface visual moderna</strong>
</p>

<p align="center">
  <a href="https://github.com/Marcolino-Dev/MOrganizador/releases/latest"><img src="https://img.shields.io/github/v/release/Marcolino-Dev/MOrganizador?style=for-the-badge&logo=github&label=Download&color=2ea44f" alt="Latest Release"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Marcolino-Dev/MOrganizador?style=for-the-badge&color=1f6feb" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python Version"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/stargazers"><img src="https://img.shields.io/github/stars/Marcolino-Dev/MOrganizador?style=for-the-badge&logo=github&color=f0883e" alt="Stars"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/issues"><img src="https://img.shields.io/github/issues/Marcolino-Dev/MOrganizador?style=for-the-badge&color=d93f0b" alt="Issues"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/pulls"><img src="https://img.shields.io/github/issues-pr/Marcolino-Dev/MOrganizador?style=for-the-badge&color=8b949e" alt="Pull Requests"></a>
</p>

<p align="center">
  <a href="https://github.com/Marcolino-Dev/MOrganizador/releases/latest"><img src="https://img.shields.io/github/downloads/Marcolino-Dev/MOrganizador/total?style=for-the-badge&logo=github&logoColor=white&label=Total%20Downloads&color=6f42c1" alt="Total Downloads"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/commits/master"><img src="https://img.shields.io/github/last-commit/Marcolino-Dev/MOrganizador?style=for-the-badge&logo=git&logoColor=white&color=24292e" alt="Last Commit"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/blob/main/SECURITY.md"><img src="https://img.shields.io/badge/Security-Policy-2c3e50?style=for-the-badge&logo=shield&logoColor=white" alt="Security Policy"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/blob/main/CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-Welcome-27ae60?style=for-the-badge&logo=github&logoColor=white" alt="PRs Welcome"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/graphs/contributors"><img src="https://img.shields.io/github/contributors/Marcolino-Dev/MOrganizador?style=for-the-badge&color=72777a" alt="Contributors"></a>
</p>

<p align="center">
  <a href="https://github.com/Marcolino-Dev/MOrganizador/pulse"><img src="https://img.shields.io/github/commit-activity/m/Marcolino-Dev/MOrganizador?style=for-the-badge&color=2ea44f" alt="Commit Activity"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador"><img src="https://img.shields.io/github/repo-size/Marcolino-Dev/MOrganizador?style=for-the-badge&color=1f6feb" alt="Repo Size"></a>
  <a href="https://github.com/Marcolino-Dev/MOrganizador/search?l=python"><img src="https://img.shields.io/github/languages/top/Marcolino-Dev/MOrganizador?style=for-the-badge&logo=python&logoColor=white&color=3776ab" alt="Top Language"></a>
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-download-e-instalação">Download</a> •
  <a href="#-uso-rápido">Uso Rápido</a> •
  <a href="#-interface-gráfica-gui">GUI</a> •
  <a href="#-linha-de-comando-cli">CLI</a> •
  <a href="#-construindo-do-código-fonte">Build</a> •
  <a href="#-contribuindo">Contribuindo</a> •
  <a href="#-segurança">Segurança</a>
</p>

---

## ✨ Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| 🎯 **Organização Inteligente** | Categoriza arquivos automaticamente por extensão (Documentos, Imagens, Instaladores, Compactados, Outros) |
| 🖥️ **Interface Gráfica (GUI)** | Janela nativa Windows com seleção de pasta, prévia colorida, barra de progresso e botão desfazer |
| ⌨️ **Linha de Comando (CLI)** | Para automação, scripts e uso em servidores/terminal |
| ✏️ **Renomeação com Data** | Prefixo `AAAA-MM-DD_` baseado na data de criação do arquivo |
| ↩️ **Desfazer Completo** | Restaura todos os arquivos para a pasta original com um clique |
| 🛡️ **Tratamento de Conflitos** | Sufixos `_1`, `_2`... automáticos para evitar sobrescrita |
| 👁️ **Modo Prévia (Dry-run)** | Simula a organização sem mover nenhum arquivo |
| 📊 **Relatório Visual** | Estatísticas por categoria em tempo real |
| 💾 **Histórico Persistente** | Salva automaticamente para permitir desfazer mesmo após fechar o programa |
| 📦 **Executável Standalone** | Arquivo `.exe` único (~13MB) - roda em qualquer Windows sem Python |

---

## 📁 Categorias Suportadas

| Categoria | Extensões | Cor na GUI |
|-----------|-----------|------------|
| **📄 Documentos** | `.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.pptx`, `.csv`, `.ods`, `.odt`, `.odp`, `.rtf`, `.md`, `.tex` | 🔵 Azul claro |
| **🖼️ Imagens** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp`, `.bmp`, `.tiff`, `.tif`, `.ico`, `.heic`, `.heif`, `.avif` | 🟠 Laranja claro |
| **⚙️ Instaladores/Executáveis** | `.exe`, `.msi`, `.dmg`, `.pkg`, `.deb`, `.rpm`, `.appimage`, `.snap`, `.flatpak`, `.apk`, `.ipa` | 🔴 Vermelho claro |
| **🗜️ Compactados** | `.zip`, `.rar`, `.tar`, `.gz`, `.7z`, `.bz2`, `.xz`, `.zst`, `.tgz`, `.tbz2`, `.txz` | 🟢 Verde claro |
| **📁 Outros** | Qualquer extensão não listada | ⚪ Cinza claro |

---

## 📥 Download e Instalação

### Opção 1: Executável Pronto (Recomendado) 🚀

1. Acesse a **[página de Releases](https://github.com/Marcolino-Dev/MOrganizador/releases/latest)**
2. Baixe `organizer_gui.exe` (interface gráfica) ou `organizer.exe` (linha de comando)
3. Execute diretamente - **não precisa instalar nada!**

> ⚠️ O Windows SmartScreen pode avisar "O Windows protegeu seu PC". Clique em **"Mais informações" → "Executar mesmo assim"**. Isso ocorre pois o executável não tem assinatura digital (custa $400/ano).

### Opção 2: Via Python (Desenvolvedores)

```bash
# Clone o repositório
git clone https://github.com/Marcolino-Dev/MOrganizador.git
cd MOrganizador

# Crie ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Instale dependências
pip install -r requirements.txt

# Execute
python organizer_gui.py --gui    # Interface gráfica
python organizer.py -r           # CLI com renomeação
```

### Opção 3: Via pip (em breve)

```bash
pip install organizador-arquivos
organizer --help
```

---

## ⚡ Uso Rápido

### Interface Gráfica (GUI)

```bash
# Duplo clique no organizer_gui.exe
# OU via terminal:
organizer_gui.exe
# OU:
python organizer_gui.py --gui
```

**Fluxo visual:**
1. 📂 **Selecione a pasta** (padrão: Downloads)
2. ✏️ **Marque "Renomear com data"** se desejar
3. 👁️ **Veja a prévia** colorida em tempo real
4. 🚀 **Clique "Iniciar Organização"**
5. 📊 **Acompanhe a barra de progresso**
6. ↩️ **Clique "Desfazer"** se quiser voltar atrás

### Linha de Comando (CLI)

```bash
# Organiza a pasta Downloads padrão com renomeação
organizer.exe -r

# Organiza pasta específica
organizer.exe "C:\Users\Você\Documentos\Bagunça"

# Simula sem mover (preview)
organizer.exe --dry-run

# Simula com renomeação
organizer.exe "C:\Pasta" --dry-run -r

# Lista categorias e extensões
organizer.exe --list-categories

# Desfaz última organização
organizer.exe --undo

# Ajuda completa
organizer.exe --help
```

**Saída exemplo:**
```
============================================================
  ORGANIZADOR AUTOMÁTICO DE ARQUIVOS v1.0.0
============================================================

============================================================
Organizando: C:\Users\Você\Downloads
============================================================
  ✓ relatorio.pdf -> Documentos/2026-11-15_relatorio.pdf
  ✓ foto.jpg -> Imagens/2026-11-10_foto.jpg
  ✓ setup.exe -> Instaladores e Executáveis/2026-11-12_setup.exe
  ✓ backup.zip -> Compactados/2026-11-01_backup.zip

============================================================
RELATÓRIO FINAL - C:\Users\Você\Downloads
============================================================
  Documentos: 15 arquivo(s)
  Imagens: 8 arquivo(s)
  Instaladores e Executáveis: 12 arquivo(s)
  Compactados: 5 arquivo(s)
  Outros: 3 arquivo(s)

  Total movido: 43 arquivo(s)
============================================================
```

---

## 🖥️ Interface Gráfica (GUI) - Detalhes

### Tela Principal

```
┌─────────────────────────────────────────────────────────────┐
│ 📁 Organizador Automático de Arquivos v1.0                  │
│    Organize seus arquivos por categoria com um clique       │
├─────────────────────────────────────────────────────────────┤
│ 📂 Pasta a Organizar                                        │
│ [C:\Users\Você\Downloads          ] [📁 Procurar] [🔄]     │
│ ☑ ✏️ Renomear com data de criação (AAAA-MM-DD_)            │
├─────────────────────────────────────────────────────────────┤
│ 👁️ Prévia da Organização                    📊 92 arquivos │
│ ┌──────────────────┬─────────────────┬──────────────────┐  │
│ │ 📄 Arquivo       │ 📁 Categoria    │ ✨ Novo Nome      │  │
│ ├──────────────────┼─────────────────┼──────────────────┤  │
│ │ relatorio.pdf    │ 📄 Documentos   │ 2026-11-15_...   │  │
│ │ foto.jpg         │ 🖼️ Imagens      │ 2026-11-10_...   │  │
│ │ setup.exe        │ ⚙️ Instaladores │ 2026-11-12_...   │  │
│ └──────────────────┴─────────────────┴──────────────────┘  │
├─────────────────────────────────────────────────────────────┤
│ ████████████████████████████████ 100%                       │
│ ✅ Concluído! 92 arquivo(s) organizado(s)                  │
├─────────────────────────────────────────────────────────────┤
│ [🚀 Iniciar Organização]  [↩ Desfazer]         [🗑️ Limpar] │
└─────────────────────────────────────────────────────────────┘
```

### Recursos Visuais

- **Cores por categoria** na tabela de prévia
- **Barra de progresso** animada durante operação
- **Status em tempo real** mostrando arquivo atual
- **Botão "Desfazer"** aparece apenas após organização bem-sucedida
- **Histórico persistente** - fecha o programa e ainda pode desfazer depois
- **Tooltips** informativos nos controles
- **Atalhos de teclado**: F5 (atualizar), Ctrl+Enter (iniciar), Ctrl+Z (desfazer), Esc (cancelar)

---

## ⌨️ Linha de Comando (CLI) - Referência

```bash
organizer.exe [PASTA] [OPÇÕES]

Argumentos:
  PASTA              Caminho da pasta (padrão: %USERPROFILE%\Downloads)

Opções:
  -r, --renomear     Adiciona prefixo AAAA-MM-DD_ (data de criação)
  --dry-run          Simula sem mover arquivos
  --list-categories  Lista todas as categorias e extensões
  --undo             Desfaz a última organização
  --clear-history    Remove o histórico de desfazer salvo
  --gui              Abre interface gráfica
  -v, --version      Mostra versão
  -h, --help         Mostra esta ajuda
  --verbose          Saída verbosa com mais detalhes
```

**Códigos de saída:**
- `0` = Sucesso
- `1` = Erro (pasta não encontrada, permissão, etc.)
- `130` = Cancelado pelo usuário (Ctrl+C)

---

## 🔧 Construindo do Código Fonte

### Pré-requisitos
- Python 3.8+
- PyInstaller: `pip install pyinstaller`

### Build CLI (Console)
```bash
pyinstaller --onefile --clean --name organizer organizer.py
# Saída: dist/organizer.exe (~9.5 MB)
```

### Build GUI (Janela Nativa)
```bash
pyinstaller --onefile --windowed --clean --name organizer_gui organizer_gui.py
# Saída: dist/organizer_gui.exe (~13 MB)
```

### Build Otimizado (Menor tamanho)
```bash
# UPX compression (instale UPX primeiro)
pyinstaller --onefile --windowed --clean --upx-dir=C:\upx --name organizer_gui organizer_gui.py
```

### Build via CI/CD (Automático)
```bash
# Crie uma tag e faça push
git tag v1.0.1
git push origin v1.0.1
# GitHub Actions faz build e cria Release automaticamente
```

---

## 📂 Estrutura do Projeto

```
organizador/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml              # CI Pipeline (lint, test, security, build)
│   │   └── build.yml           # Build & Release (tags)
│   ├── ISSUE_TEMPLATE/         # Templates de bug/feature
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── dependabot.yml          # Atualizações automáticas de dependências
│   └── CODEOWNERS              # Responsáveis por revisão
├── assets/
│   └── logo.png                # Logo do projeto
├── tests/                      # Testes unitários (pytest)
│   ├── conftest.py             # Fixtures compartilhadas
│   ├── test_categorias.py      # Testes de categorização
│   ├── test_core.py            # Testes do core
│   ├── test_cli.py             # Testes da CLI
│   └── test_gui.py             # Testes da GUI
├── organizador/                # Pacote principal
│   ├── __init__.py             # Exports públicos + versão
│   ├── core.py                 # Lógica de negócio (core)
│   ├── cli.py                  # CLI (argparse, colorama)
│   └── gui.py                  # GUI (Tkinter)
├── dist/                       # Executáveis gerados (ignorados no git)
├── build/                      # Build temporário PyInstaller (ignorado)
├── organizer.py                # Entry point CLI
├── organizer_gui.py            # Entry point GUI
├── requirements.txt            # Dependências runtime (colorama)
├── requirements-dev.txt        # Dependências de desenvolvimento
├── pyproject.toml              # Configuração projeto (build, tools)
├── .pre-commit-config.yaml     # Hooks pre-commit
├── .commitlintrc.json          # Validação Conventional Commits
├── README.md                   # Este arquivo
├── LICENSE                     # MIT License
├── CHANGELOG.md                # Histórico de versões
├── CONTRIBUTING.md             # Guia de contribuição
├── SECURITY.md                 # Política de segurança
└── .gitignore                  # Git ignore rules
```

---

## 🤝 Contribuindo

Contribuições são bem-vindas! Este é meu primeiro projeto no GitHub, então toda ajuda é valiosa.

### Como contribuir

1. **Fork** o repositório
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Faça suas alterações com **testes**
4. Commit: `git commit -m 'feat: adiciona nova funcionalidade'`
5. Push: `git push origin feature/nova-funcionalidade`
6. Abra um **Pull Request**

### Setup de Desenvolvimento

```bash
# Clone seu fork
git clone https://github.com/SEU-USUARIO/organizador.git
cd organizador

# Adicione upstream
git remote add upstream https://github.com/Marcolino-Dev/MOrganizador.git

# Ambiente virtual
python -m venv venv
venv\Scripts\activate

# Dependências de dev
pip install -r requirements-dev.txt
# ou
pip install -r requirements.txt
pip install pytest black flake8 mypy isort pre-commit bandit safety

# Instale hooks pre-commit
pre-commit install
```

### Executar Verificações Locais

```bash
# Formatação
black --check organizer.py organizer_gui.py organizador/ tests/
isort --check organizer.py organizer_gui.py organizador/ tests/

# Linting
flake8 organizer.py organizer_gui.py organizador/ tests/

# Tipagem
mypy organizer.py organizer_gui.py organizador/ --ignore-missing-imports

# Segurança
bandit -r organizer.py organizer_gui.py organizador/
safety check

# Testes
pytest tests/ -v --cov=organizador --cov=organizer --cov=organizer_gui
```

### Ideias para contribuições

- 🌍 Internacionalização (i18n) - Português/Inglês/Espanhol
- 🎨 Temas visuais (Dark/Light mode)
- ⚙️ Configuração de categorias personalizadas via JSON
- 📅 Integração com Agendador de Tarefas do Windows
- 🐧 Builds Linux (AppImage) e macOS (.dmg)
- 🧪 Testes unitários com pytest (cobertura > 80%)
- 📦 Publicação no Chocolatey, Scoop, Winget
- 🔍 Busca recursiva em subpastas (opcional)
- 📊 Logs detalhados em arquivo
- 🔔 Notificações toast do Windows

### Padrão de Commits

Usamos [Conventional Commits](https://www.conventionalcommits.org/):

| Tipo | Descrição |
|------|-----------|
| `feat:` | Nova funcionalidade |
| `fix:` | Correção de bug |
| `docs:` | Documentação |
| `style:` | Formatação (espaços, vírgulas, etc) |
| `refactor:` | Refatoração sem mudança de comportamento |
| `test:` | Testes |
| `chore:` | Manutenção (build, deps, etc) |
| `perf:` | Performance |
| `ci:` | CI/CD |
| `build:` | Build system |
| `revert:` | Reverte commit anterior |

**Exemplos:**
```
feat(gui): adiciona tema escuro na interface
fix(cli): corrige crash quando pasta não existe
docs: atualiza README com exemplos de uso
refactor(core): extrai lógica de categorização para módulo separado
test: adiciona testes para gerar_nome_unico
chore: atualiza dependências no requirements.txt
```

---

## 📋 Changelog

Veja [CHANGELOG.md](CHANGELOG.md) para histórico completo.

### v1.0.0 (2026-11-15)
- ✨ Interface gráfica completa (Tkinter)
- ✨ CLI com argparse
- ✨ 5 categorias de arquivos
- ✨ Renomeação com data de criação
- ✨ Desfazer organização completa
- ✨ Modo dry-run (preview)
- ✨ Histórico persistente em JSON
- ✨ Executáveis standalone via PyInstaller
- 📦 Build CI/CD com GitHub Actions

---

## 🛡️ Segurança

Leia nossa [Política de Segurança](SECURITY.md) para detalhes sobre:

- **Versões suportadas** e ciclo de vida
- **Como reportar vulnerabilidades** (privadamente, via Security Advisories)
- **Medidas implementadas**: Path traversal protection, input validation, symlink protection, safe history storage
- **Boas práticas** para usuários

### Resumo das Proteções

| Ameaça | Proteção |
|--------|----------|
| Path Traversal | Validação `_caminho_seguro()` em todas operações |
| Nomes perigosos | Sanitização `_sanitizar_nome()` + lista reservados Windows |
| Symlink attacks | Verificação `is_symlink()` antes de processar |
| Histórico exposto | Salvo em `LOCALAPPDATA`/`XDG_DATA_HOME`, não na pasta de trabalho |
| Dependências vuln. | Dependabot semanal + Safety no CI |

---

## 🐛 Problemas Conhecidos / FAQ

| Problema | Solução |
|----------|---------|
| "O Windows protegeu seu PC" | Mais informações → Executar mesmo assim (executável não assinado) |
| Arquivos não aparecem na prévia | Verifique se não estão ocultos (`.arquivo`) ou em subpastas |
| "Permissão negada" | Feche programas usando os arquivos / Execute como Administrador |
| Antivírus bloqueia | Adicione exceção para a pasta do executável |
| Data errada no Windows | `st_ctime` = data de criação no Windows, metadata change no Linux |
| Subpastas não organizadas | Comportamento padrão: apenas arquivos na raiz da pasta |

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**Marcolino-Dev**
- GitHub: [@Marcolino-Dev](https://github.com/marcolino-dev)

---

## ⭐ Apoie o Projeto

Se este projeto te ajudou, considere dar uma **estrela no GitHub** ⭐

Isso me motiva a continuar melhorando e ajuda outros a encontrarem o projeto!

---

## 📊 Status do Projeto

![GitHub repo size](https://img.shields.io/github/repo-size/Marcolino-Dev/MOrganizador?style=flat-square)
![GitHub language count](https://img.shields.io/github/languages/count/Marcolino-Dev/MOrganizador?style=flat-square)
![GitHub top language](https://img.shields.io/github/languages/top/Marcolino-Dev/MOrganizador?style=flat-square&logo=python)
![GitHub commit activity](https://img.shields.io/github/commit-activity/m/Marcolino-Dev/MOrganizador?style=flat-square)
![GitHub contributors](https://img.shields.io/github/contributors/Marcolino-Dev/MOrganizador?style=flat-square)

---

<p align="center">
  Feito com ❤️ e Python<br>
  <sub>Primeiro projeto no GitHub - feedbacks são muito bem-vindos!</sub>
</p>
