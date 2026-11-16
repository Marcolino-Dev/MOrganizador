<p align="center">
  <img src="assets/logo.png" alt="Organizador Logo" width="120" height="120">
</p>

<h1 align="center">Organizador Automático de Arquivos</h1>

<p align="center">
  <strong>Organize sua pasta Downloads (ou qualquer pasta) em segundos com uma interface visual moderna</strong>
</p>

<p align="center">
  <a href="https://github.com/lairm/organizador/releases/latest"><img src="https://img.shields.io/github/v/release/lairm/organizador?style=for-the-badge&logo=github&label=Download" alt="Latest Release"></a>
  <a href="https://github.com/lairm/organizador/blob/main/LICENSE"><img src="https://img.shields.io/github/license/lairm/organizador?style=for-the-badge" alt="License"></a>
  <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.8%2B-blue?style=for-the-badge&logo=python" alt="Python Version"></a>
  <a href="https://github.com/lairm/organizador/stargazers"><img src="https://img.shields.io/github/stars/lairm/organizador?style=for-the-badge&logo=github" alt="Stars"></a>
  <a href="https://github.com/lairm/organizador/issues"><img src="https://img.shields.io/github/issues/lairm/organizador?style=for-the-badge" alt="Issues"></a>
</p>

<p align="center">
  <a href="#-funcionalidades">Funcionalidades</a> •
  <a href="#-download-e-instalação">Download</a> •
  <a href="#-uso-rápido">Uso Rápido</a> •
  <a href="#-interface-gráfica-gui">GUI</a> •
  <a href="#-linha-de-comando-cli">CLI</a> •
  <a href="#-construindo-do-código-fonte">Build</a> •
  <a href="#-contribuindo">Contribuindo</a>
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
| **📄 Documentos** | `.pdf`, `.docx`, `.doc`, `.txt`, `.xlsx`, `.pptx`, `.csv` | 🔵 Azul claro |
| **🖼️ Imagens** | `.jpg`, `.jpeg`, `.png`, `.gif`, `.svg`, `.webp` | 🟠 Laranja claro |
| **⚙️ Instaladores/Executáveis** | `.exe`, `.msi`, `.dmg`, `.pkg`, `.deb`, `.rpm` | 🔴 Vermelho claro |
| **🗜️ Compactados** | `.zip`, `.rar`, `.tar`, `.gz`, `.7z` | 🟢 Verde claro |
| **📁 Outros** | Qualquer extensão não listada | ⚪ Cinza claro |

---

## 📥 Download e Instalação

### Opção 1: Executável Pronto (Recomendado) 🚀

1. Acesse a **[página de Releases](https://github.com/lairm/organizador/releases/latest)**
2. Baixe `organizer_gui.exe` (interface gráfica) ou `organizer.exe` (linha de comando)
3. Execute diretamente - **não precisa instalar nada!**

> ⚠️ O Windows SmartScreen pode avisar "O Windows protegeu seu PC". Clique em **"Mais informações" → "Executar mesmo assim"**. Isso ocorre pois o executável não tem assinatura digital (custa $400/ano).

### Opção 2: Via Python (Desenvolvedores)

```bash
# Clone o repositório
git clone https://github.com/lairm/organizador.git
cd organizador

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

---

## ⌨️ Linha de Comando (CLI) - Referência

```bash
organizer.exe [PASTA] [OPÇÕES]

Argumentos:
  PASTA              Caminho da pasta (padrão: %USERPROFILE%\Downloads)

Opções:
  -r, --renomear     Adiciona prefixo AAAA-MM-DD_ (data de criação)
  --dry-run          Simula sem mover arquivos
  --gui              Abre interface gráfica
  -v, --version      Mostra versão
  -h, --help         Mostra esta ajuda
```

**Códigos de saída:**
- `0` = Sucesso
- `1` = Erro (pasta não encontrada, permissão, etc.)

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

---

## 📂 Estrutura do Projeto

```
organizador/
├── .github/
│   └── workflows/
│       └── build.yml           # CI/CD GitHub Actions
├── assets/
│   └── logo.png                # Logo do projeto
├── dist/                       # Executáveis gerados (ignorados no git)
├── build/                      # Build temporário PyInstaller (ignorado)
├── organizer.py                # CLI principal
├── organizer_gui.py            # GUI + CLI unificado
├── requirements.txt            # Dependências (colorama)
├── requirements-dev.txt        # Dev dependencies
├── README.md                   # Este arquivo
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
├── CHANGELOG.md                # Histórico de versões
└── CONTRIBUTING.md             # Guia de contribuição
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

### Ideias para contribuições
- 🌍 Internacionalização (i18n) - Português/Inglês/Espanhol
- 🎨 Temas visuais (Dark/Light mode)
- ⚙️ Configuração de categorias personalizadas via JSON
- 📅 Agendamento automático (Windows Task Scheduler integration)
- 🐧 Suporte nativo Linux/macOS (AppImage, .dmg)
- 🧪 Testes unitários (pytest)
- 📦 Empacotamento para Chocolatey, Scoop, Winget

### Padrão de Commits
Usamos [Conventional Commits](https://www.conventionalcommits.org/):
- `feat:` nova funcionalidade
- `fix:` correção de bug
- `docs:` documentação
- `style:` formatação
- `refactor:` refatoração
- `test:` testes
- `chore:` manutenção

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

## 🐛 Problemas Conhecidos / FAQ

| Problema | Solução |
|----------|---------|
| "O Windows protegeu seu PC" | Mais informações → Executar mesmo assim (executável não assinado) |
| Arquivos não aparecem na prévia | Verifique se não estão ocultos (`.arquivo`) ou em subpastas |
| "Permissão negada" | Feche programas usando os arquivos / Execute como Administrador |
| Antivírus bloqueia | Adicione exceção para a pasta do executável |
| Data errada no Windows | `st_ctime` = data de criação no Windows, metadata change no Linux |

---

## 📄 Licença

Este projeto está licenciado sob a **MIT License** - veja [LICENSE](LICENSE) para detalhes.

---

## 👨‍💻 Autor

**lairm**
- GitHub: [@lairm](https://github.com/lairm)
- Este é meu primeiro projeto público no GitHub! ⭐

---

## ⭐ Apoie o Projeto

Se este projeto te ajudou, considere dar uma **estrela no GitHub** ⭐

Isso me motiva a continuar melhorando e ajuda outros a encontrarem o projeto!

---

<p align="center">
  Feito com ❤️ e Python<br>
  <sub>Primeiro projeto no GitHub - feedbacks são muito bem-vindos!</sub>
</p>