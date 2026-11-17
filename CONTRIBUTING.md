# Guia de Contribuição

Obrigado por considerar contribuir! Este é meu primeiro projeto no GitHub, então toda ajuda é muito bem-vinda e apreciada. ❤️

## 🚀 Como Começar

### 1. Fork e Clone
```bash
# Fork no GitHub, depois clone seu fork
git clone https://github.com/SEU-USUARIO/organizador.git
cd organizador

# Adicione upstream para sincronizar
git remote add upstream https://github.com/Marcolino-Dev/MOrganizador.git
```

### 2. Ambiente de Desenvolvimento
```bash
# Crie ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt
# ou
pip install -r requirements.txt
pip install pytest black flake8 mypy pre-commit

# Instale hooks de pre-commit
pre-commit install
```

### 3. Execute os Testes
```bash
# Testes rápidos
python -m pytest tests/ -v

# Verificação de tipos
mypy organizer.py organizer_gui.py

# Formatação
black --check organizer.py organizer_gui.py

# Linting
flake8 organizer.py organizer_gui.py
```

---

## 📝 Tipos de Contribuição

### 🐛 Reportar Bugs
- Use o template de **Bug Report** nas Issues
- Inclua: OS, versão Python, passos para reproduzir, logs/erros
- Screenshots ajudam muito!

### 💡 Sugerir Funcionalidades
- Use o template de **Feature Request**
- Explique o problema que resolve e casos de uso
- Considere se deve ser CLI, GUI ou ambos

### 🔧 Pull Requests
1. **Uma feature/fix por PR** - mantenha focado
2. **Testes** - adicione testes para novas funcionalidades
3. **Documentação** - atualize README/CHANGELOG se necessário
4. **Commits limpos** - use Conventional Commits

---

## 🎨 Padrões de Código

### Python Style
- **Black** para formatação (line-length=100)
- **Type hints** obrigatórios em funções públicas
- **Docstrings** estilo Google/NumPy
- **Imports** organizados: stdlib → third-party → local

```python
# Exemplo de função bem formatada
def processar_arquivo(
    arquivo: Path,
    pasta_destino: Path,
    renomear: bool = False
) -> ResultadoProcessamento:
    """Processa um arquivo movendo para categoria apropriada.

    Args:
        arquivo: Caminho do arquivo a processar.
        pasta_destino: Pasta base das categorias.
        renomear: Se True, adiciona prefixo de data.

    Returns:
        Resultado com status e novo caminho.

    Raises:
        PermissionError: Sem permissão para mover.
        OSError: Erro de sistema de arquivos.
    """
    ...
```

### Commits - Conventional Commits
```
<tipo>(<escopo>): <descrição curta>

[corpo opcional]

[rodapé opcional]
```

**Tipos:**
- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Documentação
- `style`: Formatação (espaços, vírgulas, etc)
- `refactor`: Refatoração sem mudança de comportamento
- `test`: Testes
- `chore`: Manutenção (build, deps, etc)
- `perf`: Performance
- `ci`: CI/CD

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

## 🏗️ Arquitetura do Projeto

```
organizer.py          # CLI puro - argparse, funções core
organizer_gui.py      # GUI (Tkinter) + CLI unificado
├── Categoria (Enum)  # 5 categorias fixas
├── EXTENSOES_CATEGORIAS (dict)  # Mapeamento ext -> Categoria
├── MovimentoArquivo (dataclass) # Para histórico desfazer
├── HistoricoOrganizacao (dataclass) # Histórico completo
├── escanear_pasta()  # Preview (não move)
├── executar_organizacao()  # Move real + retorna histórico
├── desfazer_organizacao()  # Restaura + limpa pastas vazias
└── OrganizadorGUI (class)    # Tkinter GUI completa
```

### Princípios
- **Separação CLI/GUI** - lógica core reutilizável
- **Imutabilidade** - preview não modifica nada
- **Transações** - histórico permite rollback completo
- **Threading** - GUI não trava durante operações longas
- **Fallback graceful** - colorama opcional, funciona sem

---

## 🧪 Testes

### Estrutura
```
tests/
├── test_categorias.py      # Testes de categorização
├── test_rename.py          # Testes de renomeação/conflitos
├── test_scan.py            # Testes de escaneamento/preview
├── test_organize.py        # Testes de organização real
├── test_undo.py            # Testes de desfazer
└── conftest.py             # Fixtures pytest
```

### Executar
```bash
# Todos os testes
pytest -v

# Com coverage
pytest --cov=. --cov-report=html

# Apenas testes rápidos (sem I/O real)
pytest -m "not slow"

# Testes específicos
pytest tests/test_undo.py -v
```

### Fixtures Úteis
```python
# conftest.py
@pytest.fixture
def pasta_teste(tmp_path):
    """Cria pasta temporária com arquivos de teste."""
    (tmp_path / "doc.pdf").write_text("pdf")
    (tmp_path / "img.jpg").write_bytes(b"jpg")
    (tmp_path / "app.exe").write_bytes(b"exe")
    return tmp_path
```

---

## 📦 Build e Release

### Build Local
```bash
# CLI
pyinstaller --onefile --clean --name organizer organizer.py

# GUI
pyinstaller --onefile --windowed --clean --name organizer_gui organizer_gui.py

# Testar executáveis
.\dist\organizer.exe --help
.\dist\organizer_gui.exe --help
```

### Release (Automatizado via GitHub Actions)
1. Atualize versão no código se necessário
2. `git tag v1.0.1`
3. `git push origin v1.0.1`
4. GitHub Actions faz build e cria Release automaticamente

---

## 🎯 Boas Práticas

### Antes de Submeter PR
- [ ] `pytest` passa
- [ ] `mypy` sem erros
- [ ] `black --check` passa
- [ ] `flake8` passa
- [ ] Testado manualmente (GUI + CLI)
- [ ] CHANGELOG.md atualizado (seção Unreleased)
- [ ] README atualizado se nova feature visível

### Code Review
- Seja respeitoso e construtivo
- Foque no código, não na pessoa
- Sugira melhorias, não apenas critique
- Aprove se estiver bom, peça mudanças se necessário

---

## 💬 Comunicação

- **Issues**: Bugs, features, dúvidas
- **Discussions**: Ideias gerais, perguntas, showcase
- **PRs**: Código pronto para review

---

## 📚 Recursos Úteis

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

---

## ❓ Dúvidas?

Abra uma **Issue** com label `question` ou inicie uma **Discussion**.

Obrigado por contribuir! 🎉

---

*Primeiro projeto no GitHub - sua paciência e feedback são muito valiosos!*