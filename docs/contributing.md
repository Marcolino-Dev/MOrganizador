# Guia de Contribuição - Documentação Técnica

## Visão Rápida

Este documento complementa o [CONTRIBUTING.md](../CONTRIBUTING.md) principal com detalhes técnicos para desenvolvedores.

## Ambiente de Desenvolvimento

### Pré-requisitos
- Python 3.8+ (recomendado 3.11+)
- Git
- Editor com suporte a EditorConfig (VS Code, PyCharm, etc.)

### Setup Rápido (Windows PowerShell)
```powershell
# 1. Clone e entre na pasta
git clone https://github.com/Marcolino-Dev/MOrganizador.git
cd organizador

# 2. Setup completo (venv + deps + hooks)
.\dev.ps1 setup

# 3. Verifique se tudo funciona
.\dev.ps1 test-fast
.\dev.ps1 run-gui
```

### Setup com Make (Linux/macOS/WSL/Git Bash)
```bash
make setup
make test-fast
make run-gui
```

### Setup com Just (Cross-platform)
```bash
just setup
just test-fast
just run-gui
```

## Padrões de Código

### Type Hints (Obrigatório)
```python
# ✅ Bom - Type hints completos
def processar_arquivo(
    arquivo: Path,
    pasta_destino: Path,
    renomear: bool = False
) -> ResultadoProcessamento:
    """Processa um arquivo movendo para categoria apropriada."""
    ...

# ❌ Ruim - Sem type hints
def processar_arquivo(arquivo, pasta_destino, renomear=False):
    ...
```

### Docstrings (Google Style)
```python
def mover_arquivo(origem: Path, destino: Path) -> bool:
    """Move arquivo com tratamento de conflitos.

    Args:
        origem: Caminho do arquivo origem.
        destino: Caminho de destino desejado.

    Returns:
        True se movido com sucesso, False se cancelado.

    Raises:
        PermissionError: Sem permissão para mover.
        OSError: Erro de sistema de arquivos.
    """
    ...
```

### Imports Organizados
```python
# 1. Stdlib
import json
import logging
import os
from pathlib import Path
from typing import Optional

# 2. Third-party
import colorama
import pytest

# 3. Local
from .core import Categoria, executar_organizacao
from . import __version__
```

## Testes

### Estrutura
```
tests/
├── conftest.py              # Fixtures compartilhadas
├── test_categorias.py       # Testes de categorização
├── test_core.py             # Testes do core (movimento, histórico, etc)
├── test_cli.py              # Testes da CLI
└── test_gui.py              # Testes da GUI (mocks)
```

### Fixtures Úteis (conftest.py)
```python
@pytest.fixture
def pasta_teste():
    """Pasta temporária com arquivos de todas categorias."""
    ...

@pytest.fixture
def pasta_vazia():
    """Pasta temporária vazia."""
    ...

@pytest.fixture
def mock_historico(pasta_teste):
    """Histórico preenchido para testes de desfazer."""
    ...
```

### Executar Testes
```bash
# Todos com coverage
pytest --cov=organizador --cov=organizer --cov=organizer_gui --cov-report=html

# Apenas unitários rápidos
pytest -m "not slow and not integration"

# Específico
pytest tests/test_core.py::TestExecutarOrganizacao -v

# Com output detalhado
pytest -v --tb=long
```

### Escrevendo Novos Testes
```python
class TestNovaFuncionalidade:
    """Testes para nova funcionalidade X."""

    def test_caso_basico(self, pasta_teste):
        """Testa caso de uso principal."""
        resultado = nova_funcao(pasta_teste)
        assert resultado.sucesso is True

    def test_edge_case_arquivo_vazio(self, pasta_teste):
        """Testa arquivo vazio."""
        (pasta_teste / "vazio.txt").write_bytes(b"")
        resultado = nova_funcao(pasta_teste)
        assert resultado.processados == 1

    def test_erro_permissao(self, pasta_teste, monkeypatch):
        """Testa erro de permissão simulado."""
        def mock_move(*args, **kwargs):
            raise PermissionError("Mocked")
        monkeypatch.setattr("shutil.move", mock_move)

        with pytest.raises(PermissaoError):
            nova_funcao(pasta_teste)
```

## Git Workflow

### Branches
```
main/master          # Produção estável
feature/xyz          # Nova funcionalidade
fix/abc              # Correção de bug
docs/readme-update   # Documentação
chore/deps-update    # Manutenção
```

### Commits (Conventional Commits)
```bash
# Feature
git commit -m "feat(gui): adiciona tema escuro na interface"

# Fix
git commit -m "fix(cli): corrige crash quando pasta não existe"

# Docs
git commit -m "docs: atualiza README com exemplos de uso"

# Refactor
git commit -m "refactor(core): extrai lógica de categorização"

# Test
git commit -m "test: adiciona testes para gerar_nome_unico"

# Chore
git commit -m "chore: atualiza dependências no requirements.txt"
```

### Pull Request Checklist
- [ ] `pytest` passa (coverage ≥ 80%)
- [ ] `mypy` sem erros
- [ ] `black --check` passa
- [ ] `flake8` passa
- [ ] `bandit` sem issues high/medium
- [ ] Testado manualmente (CLI + GUI)
- [ ] CHANGELOG.md atualizado (Unreleased)
- [ ] README.md atualizado se feature visível
- [ ] Commits seguem Conventional Commits
- [ ] Pre-commit hooks passam localmente

## Code Review Guidelines

### O que revisar
1. **Corretude**: Lógica faz o que se propõe?
2. **Edge cases**: Arquivos vazios, nomes longos, Unicode, permissões?
3. **Segurança**: Path traversal, symlinks, validação de input?
4. **Performance**: O(n²) desnecessário? I/O excessivo?
5. **Legibilidade**: Nomes claros, comentários onde necessário?
6. **Testes**: Cobertura adequada? Testes de erro?

### Comentários Úteis
```markdown
# ✅ Bom
> Sugiro usar `pathlib.Path` em vez de `os.path` aqui para consistência.
> Veja linha 42 em core.py

# ✅ Bom
> Edge case: o que acontece se `destino` já existe e é um diretório?
> Sugiro adicionar teste.

# ❌ Ruim
> Isso está errado.
> Mude isso.
```

## Segurança

### Checklist de Segurança por PR
- [ ] Validação de caminho (`_caminho_seguro`) em novas operações de arquivo
- [ ] Sanitização de nomes (`_sanitizar_nome`) para inputs de usuário
- [ ] Verificação de symlink (`is_symlink()`) antes de processar
- [ ] Não logar dados sensíveis (caminhos completos em produção)
- [ ] Dependências atualizadas (Dependabot + Safety)

### Reportando Vulnerabilidades
**NÃO abra issue pública.** Use:
- GitHub Security Advisories (aba Security → Report a vulnerability)
- Email: security@lairm.dev

## Release Process

### Versionamento (SemVer)
- **Patch** (1.0.0 → 1.0.1): Bug fixes, docs, chore
- **Minor** (1.0.0 → 1.1.0): Novas features, backward compatible
- **Major** (1.0.0 → 2.0.0): Breaking changes

### Criar Release
```bash
# 1. Atualize versão no código
just bump-patch  # ou bump-minor / bump-major

# 2. Atualize CHANGELOG.md (mova Unreleased para versão)

# 3. Commit + Tag
git add -A
git commit -m "chore: release v1.0.1"
git tag v1.0.1
git push origin master --tags

# 4. GitHub Actions faz o resto:
#    - Build executáveis Windows
#    - Cria Release no GitHub
#    - Anexa executáveis + wheel + sdist
```

## Debugging

### Logs Detalhados
```bash
# CLI
python organizer.py -v --verbose "C:\Pasta"

# GUI (console)
python organizer_gui.py --gui 2>&1 | tee gui.log
```

### Breakpoints (VS Code)
```json
// .vscode/launch.json
{
    "configurations": [
        {
            "name": "Debug CLI",
            "type": "python",
            "request": "launch",
            "module": "organizer",
            "args": ["--dry-run", "C:\\Teste"],
            "console": "integratedTerminal"
        },
        {
            "name": "Debug GUI",
            "type": "python",
            "request": "launch",
            "module": "organizer_gui",
            "args": ["--gui"],
            "console": "integratedTerminal"
        }
    ]
}
```

### Testes Isolados
```bash
# Debug test específico
pytest tests/test_core.py::TestExecutarOrganizacao::test_organiza_arquivos -v -s --tb=long

# Com pdb em falha
pytest tests/ -x --pdb
```

## Performance

### Profiling
```bash
# CPU profile
python -m cProfile -o profile.stats organizer.py "C:\Pasta Grande"
python -c "import pstats; p = pstats.Stats('profile.stats'); p.sort_stats('cumulative').print_stats(20)"

# Memory profile (instale memory_profiler)
python -m memory_profiler organizer.py "C:\Pasta"
```

### Benchmarks
```bash
# Comparar antes/depois
hyperfine --warmup 3 'python organizer.py "C:\Pasta"' 'python organizer_old.py "C:\Pasta"'
```

## Acessibilidade (GUI)

### Checklist
- [ ] Contraste de cores ≥ 4.5:1 (WCAG AA)
- [ ] Navegação por teclado (Tab, Setas, Enter, Esc)
- [ ] Tooltips em todos controles
- [ ] Textos não apenas em cores (ícones + texto)
- [ ] Foco visível
- [ ] Tamanho de fonte respeita configuração do sistema

## Internacionalização (Futuro)

### Preparação
```python
# Use strings extraíveis
from gettext import gettext as _

msg = _("Arquivo movido com sucesso")

# Para formatação
msg = _("Movido {count} arquivos").format(count=n)
```

### Estrutura Futura
```
organizador/
├── locales/
│   ├── pt_BR/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po
│   │       └── messages.mo
│   ├── en_US/
│   └── es_ES/
```

## Recursos Úteis

- [Python Type Hints](https://docs.python.org/3/library/typing.html)
- [Tkinter Docs](https://docs.python.org/3/library/tkinter.html)
- [PyInstaller Manual](https://pyinstaller.org/en/stable/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [OWASP Secure Coding](https://cheatsheetseries.owasp.org/)