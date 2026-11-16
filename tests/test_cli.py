"""
Testes para CLI do Organizador.
"""

from unittest.mock import MagicMock, patch

from organizador.cli import (
    criar_parser,
    executar_dry_run,
    imprimir_cabecalho,
    listar_categorias,
    main,
)
from organizador.core import Categoria


class TestCriarParser:
    """Testes para criação do parser de argumentos."""

    def test_parser_criado(self):
        parser = criar_parser()
        assert parser.prog == "organizer"
        assert "Organizador Automático de Arquivos" in parser.description

    def test_argumento_pasta_padrao(self, pasta_teste):
        parser = criar_parser()
        args = parser.parse_args([])
        assert args.pasta == str(pasta_teste) or "Downloads" in args.pasta

    def test_flag_renomear(self):
        parser = criar_parser()
        args = parser.parse_args(["-r"])
        assert args.renomear is True
        args = parser.parse_args(["--renomear"])
        assert args.renomear is True

    def test_flag_dry_run(self):
        parser = criar_parser()
        args = parser.parse_args(["--dry-run"])
        assert args.dry_run is True
        args = parser.parse_args(["--preview"])
        assert args.dry_run is True

    def test_flag_list_categories(self):
        parser = criar_parser()
        args = parser.parse_args(["--list-categories"])
        assert args.list_categories is True

    def test_flag_undo(self):
        parser = criar_parser()
        args = parser.parse_args(["--undo"])
        assert args.undo is True

    def test_flag_clear_history(self):
        parser = criar_parser()
        args = parser.parse_args(["--clear-history"])
        assert args.clear_history is True

    def test_flag_verbose(self):
        parser = criar_parser()
        args = parser.parse_args(["--verbose"])
        assert args.verbose is True


class TestImprimirCabecalho:
    """Testes para impressão do cabeçalho."""

    def test_imprime_sem_erro(self, capsys):
        imprimir_cabecalho()
        captured = capsys.readouterr()
        assert "ORGANIZADOR AUTOMÁTICO DE ARQUIVOS" in captured.out
        assert "=" * 60 in captured.out


class TestListarCategorias:
    """Testes para listagem de categorias."""

    def test_lista_todas_categorias(self, capsys):
        listar_categorias()
        captured = capsys.readouterr()
        assert "CATEGORIAS SUPORTADAS" in captured.out
        for cat in Categoria:
            assert cat.value in captured.out
            assert cat.icone in captured.out


class TestExecutarDryRun:
    """Testes para modo dry-run."""

    def test_dry_run_vazio(self, pasta_vazia, capsys):
        resultado = executar_dry_run(pasta_vazia, renomear=False, verbose=False)
        assert resultado == 0
        captured = capsys.readouterr()
        assert "Nenhum arquivo encontrado" in captured.out

    def test_dry_run_com_arquivos(self, pasta_teste, capsys):
        resultado = executar_dry_run(pasta_teste, renomear=False, verbose=False)
        assert resultado == 0
        captured = capsys.readouterr()
        assert "PRÉVIA (DRY-RUN)" in captured.out
        assert "Total:" in captured.out

    def test_dry_run_com_renomear(self, pasta_teste, capsys):
        resultado = executar_dry_run(pasta_teste, renomear=True, verbose=False)
        assert resultado == 0
        captured = capsys.readouterr()
        assert "Renomeação: ATIVADA" in captured.out


class TestMain:
    """Testes para função main da CLI."""

    def test_main_list_categories(self, capsys):
        with patch("sys.argv", ["organizer", "--list-categories"]):
            resultado = main()
        assert resultado == 0
        captured = capsys.readouterr()
        assert "CATEGORIAS SUPORTADAS" in captured.out

    def test_main_pasta_inexistente(self, capsys):
        with patch("sys.argv", ["organizer", "/pasta/inexistente"]):
            resultado = main()
        assert resultado == 1
        captured = capsys.readouterr()
        assert "Pasta não encontrada" in captured.out

    def test_main_arquivo_como_pasta(self, pasta_teste, capsys):
        arquivo = pasta_teste / "relatorio.pdf"
        with patch("sys.argv", ["organizer", str(arquivo)]):
            resultado = main()
        assert resultado == 1
        captured = capsys.readouterr()
        assert "não é uma pasta" in captured.out

    def test_main_dry_run(self, pasta_teste, capsys):
        with patch("sys.argv", ["organizer", str(pasta_teste), "--dry-run"]):
            resultado = main()
        assert resultado == 0
        captured = capsys.readouterr()
        assert "PRÉVIA (DRY-RUN)" in captured.out

    def test_main_undo_sem_historico(self, capsys):
        with patch("organizador.core.carregar_historico", return_value=None):
            with patch("sys.argv", ["organizer", "--undo"]):
                resultado = main()
        assert resultado == 1
        captured = capsys.readouterr()
        assert "Nenhum histórico para desfazer" in captured.out

    def test_main_clear_history(self, capsys):
        with patch("organizador.cli.remover_historico", return_value=True) as mock_remover:
            with patch("sys.argv", ["organizer", "--clear-history"]):
                resultado = main()
        assert resultado == 0
        mock_remover.assert_called_once()
        captured = capsys.readouterr()
        assert "Histórico removido" in captured.out

    def test_main_keyboard_interrupt(self, pasta_teste, capsys):
        with patch("organizador.cli.executar_organizacao", side_effect=KeyboardInterrupt):
            with patch("sys.argv", ["organizer", str(pasta_teste)]):
                resultado = main()
        assert resultado == 130
        captured = capsys.readouterr()
        assert "cancelada pelo usuário" in captured.out


class TestMainIntegration:
    """Testes de integração da CLI (mockando core)."""

    def test_organiza_com_sucesso(self, pasta_teste, capsys):
        mock_historico = MagicMock()
        mock_historico.total_arquivos = 5
        mock_historico.movimentos = [
            MagicMock(categoria="Documentos"),
            MagicMock(categoria="Documentos"),
            MagicMock(categoria="Imagens"),
            MagicMock(categoria="Instaladores e Executáveis"),
            MagicMock(categoria="Compactados"),
        ]

        with patch("organizador.cli.executar_organizacao", return_value=mock_historico):
            with patch("organizador.cli.salvar_historico") as mock_salvar:
                with patch("sys.argv", ["organizer", str(pasta_teste), "-r"]):
                    resultado = main()

        assert resultado == 0
        mock_salvar.assert_called_once()
        captured = capsys.readouterr()
        assert "RELATÓRIO FINAL" in captured.out
        assert "5 arquivo(s)" in captured.out

    def test_erro_pasta_invalida(self, capsys, tmp_path):
        """Testa erro quando pasta não existe."""
        pasta_inexistente = tmp_path / "nao_existe"
        with patch("sys.argv", ["organizer", str(pasta_inexistente)]):
            resultado = main()
        assert resultado == 1
        captured = capsys.readouterr()
        assert "Pasta não encontrada" in captured.out

    def test_erro_permissao(self, capsys, tmp_path):
        """Testa erro de permissão simulado."""
        from organizador.core import PermissaoError

        pasta_valida = tmp_path / "pasta_valida"
        pasta_valida.mkdir()

        with patch(
            "organizador.cli.executar_organizacao", side_effect=PermissaoError("Permissão negada")
        ):
            with patch("sys.argv", ["organizer", str(pasta_valida)]):
                resultado = main()
        assert resultado == 1
        captured = capsys.readouterr()
        assert "Erro de permissão" in captured.out
        assert "Administrador" in captured.out


class TestArgumentosCombinados:
    """Testes para combinações de argumentos."""

    def test_dry_run_com_renomear(self, pasta_teste, capsys):
        with patch("sys.argv", ["organizer", str(pasta_teste), "--dry-run", "-r"]):
            resultado = main()
        assert resultado == 0
        captured = capsys.readouterr()
        assert "Renomeação: ATIVADA" in captured.out
        assert "PRÉVIA (DRY-RUN)" in captured.out

    def test_pasta_explicita(self, pasta_teste, capsys):
        with patch("organizador.cli.executar_organizacao") as mock_exec:
            mock_exec.return_value = MagicMock(total_arquivos=0, movimentos=[])
            with patch("organizador.cli.salvar_historico"):
                with patch("sys.argv", ["organizer", str(pasta_teste)]):
                    resultado = main()
        assert resultado == 0
        # Verifica se pasta foi passada corretamente
        mock_exec.assert_called_once()
        args, kwargs = mock_exec.call_args
        assert str(pasta_teste) in str(args[0])
