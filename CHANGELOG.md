# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

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
- 🧪 Testes unitários com pytest
- 📦 Publicação no Chocolatey, Scoop, Winget
- 🔍 Busca recursiva em subpastas (opcional)
- 📊 Logs detalhados em arquivo
- 🔔 Notificações toast do Windows