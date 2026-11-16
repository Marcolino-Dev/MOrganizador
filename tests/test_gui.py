"""
Testes para GUI (Interface Gráfica).

Nota: Testes completos de GUI com Tkinter requerem display.
Estes testes verificam a lógica de negócio da classe OrganizadorGUI
sem inicializar a janela completa.
"""

from unittest.mock import patch

import pytest

# Skip GUI tests se não houver display (headless CI)
try:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    root.destroy()
    TKINTER_DISPONIVEL = True
except Exception:
    TKINTER_DISPONIVEL = False


pytestmark = pytest.mark.skipif(
    not TKINTER_DISPONIVEL, reason="Tkinter não disponível ou sem display"
)


class TestOrganizadorGUILogica:
    """Testes para lógica da GUI sem UI real."""

    def test_formatar_tamanho(self):
        """Testa formatação de tamanho."""
        from organizador.gui import OrganizadorGUI

        # Cria instância mockada
        with patch("tkinter.Tk"), patch("tkinter.ttk.Style"):
            gui = OrganizadorGUI.__new__(OrganizadorGUI)
            gui.CORES = {}

            # Testa método
            assert gui._formatar_tamanho(500) == "500.0 B"
            assert gui._formatar_tamanho(1024) == "1.0 KB"
            assert gui._formatar_tamanho(1024 * 1024) == "1.0 MB"

    def test_categoria_tags(self):
        """Testa que Categoria enum tem tags corretas para treeview."""
        from organizador.core import Categoria

        assert Categoria.DOCUMENTOS.name.lower() == "documentos"
        assert Categoria.IMAGENS.name.lower() == "imagens"
        assert Categoria.INSTALADORES.name.lower() == "instaladores"
        assert Categoria.COMPACTADOS.name.lower() == "compactados"
        assert Categoria.OUTROS.name.lower() == "outros"


class TestIntegracaoGUI:
    """Testes de integração com Tkinter real (requer display)."""

    @pytest.fixture
    def root(self):
        """Cria root Tkinter para testes."""
        root = tk.Tk()
        root.withdraw()  # Esconde janela
        yield root
        try:
            root.destroy()
        except Exception:
            pass

    def test_instancia_gui(self, root):
        """Testa criação de instância da GUI."""
        from organizador.gui import OrganizadorGUI

        app = OrganizadorGUI(root)
        assert app is not None
        assert app.root == root
        assert app.pasta_selecionada.get() != ""
        assert app.renomear_var.get() is True
        assert app.organizando is False

    def test_atualizar_preview_pasta_vazia(self, root, pasta_vazia):
        """Testa preview com pasta vazia."""
        from organizador.gui import OrganizadorGUI

        app = OrganizadorGUI(root)
        app.pasta_selecionada.set(str(pasta_vazia))
        app.atualizar_preview()

        assert len(app.movimentos_preview) == 0
        assert "Nenhum arquivo" in app.lbl_estatisticas.cget("text")

    def test_atualizar_preview_com_arquivos(self, root, pasta_teste):
        """Testa preview com arquivos."""
        from organizador.gui import OrganizadorGUI

        app = OrganizadorGUI(root)
        app.pasta_selecionada.set(str(pasta_teste))
        app.atualizar_preview()

        assert len(app.movimentos_preview) > 0
        assert "arquivo(s)" in app.lbl_estatisticas.cget("text")

    def test_selecionar_pasta_invalida(self, root):
        """Testa comportamento com pasta inválida."""
        from organizador.gui import OrganizadorGUI

        app = OrganizadorGUI(root)
        app.pasta_selecionada.set("/pasta/inexistente")
        app.atualizar_preview()

        assert "inválida" in app.lbl_estatisticas.cget("text")
        assert str(app.btn_iniciar["state"]) == "disabled"


# Teste de fumaça para verificar imports
def test_imports_gui():
    """Verifica se módulo GUI importa sem erros."""
    from organizador import gui

    assert hasattr(gui, "OrganizadorGUI")
    assert hasattr(gui, "main_gui")
