# Arquitetura do Organizador Automático de Arquivos

## Visão Geral

O Organizador é um utilitário desktop para categorização automática de arquivos por extensão, com interface de linha de comando (CLI) e interface gráfica (GUI) nativa Windows.

```
┌─────────────────────────────────────────────────────────────┐
│                      Organizador                            │
├─────────────────────┬───────────────────────────────────────┤
│      CLI            │           GUI (Tkinter)               │
│  (organizer.py)     │      (organizer_gui.py)               │
├─────────────────────┴───────────────────────────────────────┤
│                    Core Module                              │
│  (organizador/core.py)                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐  │
│  │Categoriza│ │ Renomeia │ │  Move    │ │  Histórico   │  │
│  │  ção     │ │  Data    │ │  Arquivos│ │  Persistente │  │
│  └──────────┘ └──────────┘ └──────────┘ └──────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## Componentes Principais

### 1. Core (`organizador/core.py`)
**Responsabilidade**: Toda lógica de negócio compartilhada.

**Classes/Enums**:
- `Categoria` (Enum): 5 categorias fixas com ícones e cores
- `MovimentoArquivo` (dataclass): Registro de um movimento para desfazer
- `HistoricoOrganizacao` (dataclass): Histórico completo com serialização JSON
- Exceções customizadas: `OrganizadorError`, `PastaInvalidaError`, `PermissaoError`

**Funções Principais**:
- `escanear_pasta()`: Preview (dry-run) - não move arquivos
- `executar_organizacao()`: Move real + retorna histórico
- `desfazer_organizacao()`: Restaura + limpa pastas vazias
- `salvar_historico()` / `carregar_historico()` / `remover_historico()`: Persistência

**Segurança**:
- `_caminho_seguro()`: Previne path traversal
- `_validar_nome_arquivo()`: Valida nomes perigosos (reservados Windows)
- `_sanitizar_nome()`: Sanitiza nomes de arquivo
- Verificação de symlinks antes de processar

### 2. CLI (`organizador/cli.py` + `organizer.py`)
**Responsabilidade**: Interface de linha de comando com argparse.

**Features**:
- Argumentos posicionais e opções (`-r`, `--dry-run`, `--undo`, `--list-categories`)
- Colorama para saída colorida (fallback gracioso se não instalado)
- Callbacks de progresso com barra ASCII
- Códigos de saída apropriados (0, 1, 130)

### 3. GUI (`organizador/gui.py` + `organizer_gui.py`)
**Responsabilidade**: Interface gráfica nativa Windows (Tkinter).

**Arquitetura**:
- `OrganizadorGUI` class: Toda lógica de UI + threading
- Threading para não travar UI durante operações longas
- Callbacks thread-safe via `root.after()`
- Treeview com cores por categoria
- Tooltips, atalhos de teclado, drag-and-drop ready

**Componentes UI**:
- Header com título
- Seletor de pasta (Entry + Browse + Refresh)
- Opção renomear com checkbox
- Preview Treeview (4 colunas: Arquivo, Categoria, Novo Nome, Tamanho)
- Toolbar (Expandir, Colapsar, Copiar Lista)
- Progressbar + Status label
- Botões: Iniciar (Primário), Desfazer (Perigo), Limpar Histórico (Secundário)

## Fluxo de Dados

### Organização (CLI/GUI)
```
1. Input: Pasta + Opção Renomear
         │
         ▼
2. escanear_pasta() → Lista de movimentos planejados
         │
         ▼
3. [GUI] Preview no Treeview  [CLI] Dry-run output
         │
         ▼
4. Usuário confirma
         │
         ▼
5. executar_organizacao() → Move arquivos + retorna HistoricoOrganizacao
         │
         ▼
6. salvar_historico() → JSON em LOCALAPPDATA/XDG_DATA_HOME
         │
         ▼
7. Relatório final + Botão Desfazer habilitado
```

### Desfazer
```
1. carregar_historico() → HistoricoOrganizacao
         │
         ▼
2. desfazer_organizacao() → Move de volta + remove pastas vazias
         │
         ▼
3. remover_historico() → Apaga JSON
```

## Estrutura de Dados - Histórico

```json
{
  "versao": "1.0",
  "timestamp": "2026-11-15T14:30:00.123456",
  "pasta_base": "C:\\Users\\Usuario\\Downloads",
  "renomear": true,
  "movimentos": [
    {
      "origem": "C:\\Users\\Usuario\\Downloads\\relatorio.pdf",
      "destino": "C:\\Users\\Usuario\\Downloads\\Documentos\\2026-11-15_relatorio.pdf",
      "categoria": "Documentos"
    }
  ]
}
```

## Categorias e Extensões

| Categoria | Extensões (principais) |
|-----------|------------------------|
| Documentos | .pdf, .docx, .txt, .xlsx, .pptx, .csv, .md, .ods, .odt |
| Imagens | .jpg, .png, .gif, .svg, .webp, .bmp, .tiff, .heic |
| Instaladores | .exe, .msi, .dmg, .deb, .rpm, .appimage, .apk |
| Compactados | .zip, .rar, .7z, .tar, .gz, .bz2, .xz |
| Outros | Tudo não listado acima |

## Threading Model (GUI)

```
Main Thread (UI)          Worker Thread (Operação)
┌─────────────────┐       ┌──────────────────────┐
│ OrganizadorGUI  │       │ _executar_organizacao │
│                 │       │ _thread()             │
│ - Treeview      │       │                      │
│ - Progressbar   │       │ - executar_organizacao│
│ - Buttons       │       │ - callback_progresso  │
│                 │       │   (via root.after)    │
└────────┬────────┘       └──────────┬───────────┘
         │                            │
         │      root.after(0, cb)     │
         │◄───────────────────────────│
         │                            │
         │  Atualiza UI               │
         ▼                            ▼
```

## Persistência de Histórico

**Localização**:
- Windows: `%LOCALAPPDATA%\organizador-arquivos\.organizador_historico.json`
- Linux/macOS: `~/.local/share/organizador-arquivos/.organizador_historico.json`

**Motivação**: Não poluir pasta do usuário, sobreviver a reinicializações, seguro contra exclusão acidental.

## Build e Distribuição

### PyInstaller Specs
- CLI: `--onefile --clean --name organizer organizer.py` (~9.5 MB)
- GUI: `--onefile --windowed --clean --name organizer_gui organizer_gui.py` (~13 MB)

### CI/CD (GitHub Actions)
- **CI Pipeline** (ci.yml): Lint, type-check, test, security, build package
- **Build & Release** (build.yml): Windows executables + GitHub Release on tags
- **Dependabot**: Weekly dependency updates
- **Pre-commit**: Local quality gates

## Compatibilidade

| Plataforma | CLI | GUI | Build |
|------------|-----|-----|-------|
| Windows 10/11 | ✅ | ✅ (Native) | ✅ .exe |
| Linux | ✅ | ⚠️ (Tkinter) | 🔄 AppImage (planned) |
| macOS | ✅ | ⚠️ (Tkinter) | 🔄 .dmg (planned) |

## Princípios de Design

1. **Separação de responsabilidades**: Core reutilizável, CLI/GUI finos
2. **Imutabilidade no preview**: `escanear_pasta()` não modifica nada
3. **Transacional**: Histórico permite rollback completo
4. **Fail-fast**: Validações early, erros claros
5. **Graceful degradation**: Colorama opcional, GUI Windows-first
6. **Segurança first**: Path traversal, symlinks, nomes reservados
7. **Cross-platform core**: Lógica funciona em Windows/Linux/macOS