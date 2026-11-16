"""
Testes para CLI (Interface de Linha de Comando).
"""

from unittest.mock import patch

import pytest

from organizador.cli import (
    criar_parser,
    executar_dry_run,
    imprimir_cabecalho,
    listar_categorias,
    main,
)


class TestCriarParser:
    """Testes para criação do parser de argumentos."""

    def test_parser_criado(self):
        parser = criar_parser()
        assert parser is not None
        assert parser.prog == "organizer"

    def test_argumento_pasta_padrao(self):
        parser = criar_parser()
        args = parser.parse_args([])
        assert args.pasta is not None
        assert "Downloads" in args.pasta or "home" in args.pasta.lower()

    def test_argumento_pasta_customizada(self):
        parser = criar_parser()
        args = parser.parse_args(["/caminho/customizado"])
        assert args.pasta == "/caminho/customizado"

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

    def test_flag_verbose(self):
        parser = criar_parser()
        args = parser.parse_args(["--verbose"])
        assert args.verbose is True

    def test_version(self):
        parser = criar_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["-v"])
        with pytest.raises(SystemExit):
            parser.parse_args(["--version"])


class TestImprimirCabecalho:
    """Testes para impressão do cabeçalho."""

    def test_imprime_sem_erro(self, capsys):
        imprimir_cabecalho()
        captured = capsys.readouterr()
        assert "ORGANIZADOR AUTOMÁTICO DE ARQUIVOS" in captured.out
        assert "=" * 60 in captured.out


class TestListarCategorias:
    """Testes para listagem de categorias."""

    def test_lista_sem_erro(self, capsys):
        listar_categorias()
        captured = capsys.readouterr()
        assert "CATEGORIAS SUPORTADAS" in captured.out
        assert "Documentos" in captured.out
        assert "Imagens" in captured.out
        assert "Instaladores" in captured.out
        assert "Compactados" in captured.out
        assert "Outros" in captured.out


class TestExecutarDryRun:
    """Testes para modo dry-run."""

    def test_pasta_vazia(self, pasta_vazia, capsys):
        result = executar_dry_run(pasta_vazia, renomear=False, verbose=False)
        assert result == 0
        captured = capsys.readouterr()
        assert "Nenhum arquivo encontrado" in captured.out

    def test_com_arquivos(self, pasta_teste, capsys):
        result = executar_dry_run(pasta_teste, renomear=False, verbose=False)
        assert result == 0
        captured = capsys.readouterr()
        assert "PRÉVIA" in captured.out
        assert "Total:" in captured.out

    def test_com_renomear(self, pasta_teste, capsys):
        result = executar_dry_run(pasta_teste, renomear=True, verbose=False)
        assert result == 0
        captured = capsys.readouterr()
        assert "Renomeação: ATIVADA" in captured.out

    def test_verbose(self, pasta_teste, capsys):
        result = executar_dry_run(pasta_teste, renomear=False, verbose=True)
        assert result == 0
        captured = capsys.readouterr()
        # Verbose mostra tamanho
        assert "KB" in captured.out or "B" in captured.out


class TestMain:
    """Testes para função main."""

    def test_list_categories_exit_0(self):
        with patch("organizador.cli.listar_categorias") as mock_list:
            result = main(["--list-categories"])
            assert result == 0
            mock_list.assert_called_once()

    def test_pasta_inexistente_exit_1(self):
        result = main(["/pasta/que/nao/existe"])
        assert result == 1

    def test_help_exit_0(self):
        with pytest.raises(SystemExit) as exc:
            main(["-h"])
        assert exc.value.code == 0

    def test_dry_run_pasta_valida(self, pasta_teste):
        with patch("organizador.cli.executar_dry_run", return_value=0) as mock_dry:
            result = main([str(pasta_teste), "--dry-run"])
            assert result == 0
            mock_dry.assert_called_once()

    def test_keyboard_interrupt_exit_130(self, pasta_teste):
        with patch("organizador.cli.executar_organizacao", side_effect=KeyboardInterrupt()):
            result = main([str(pasta_teste)])
            assert result == 130

    def test_organizador_error_exit_1(self, pasta_teste):
        from organizador.core import OrganizadorError

        with patch(
            "organizador.cli.executar_organizacao", side_effect=OrganizadorError("Erro teste")
        ):
            result = main([str(pasta_teste)])
            assert result == 1

    def test_pasta_invalida_exit_1(self, pasta_teste):
        from organizador.core import PastaInvalidaError

        with patch(
            "organizador.cli.executar_organizacao", side_effect=PastaInvalidaError("Pasta inválida")
        ):
            result = main([str(pasta_teste)])
            assert result == 1

    def test_permissao_error_exit_1(self, pasta_teste):
        from organizador.core import PermissaoError

        with patch(
            "organizador.cli.executar_organizacao", side_effect=PermissaoError("Sem permissão")
        ):
            result = main([str(pasta_teste)])
            assert result == 1


class TestMainIntegration:
    """Testes de integração da CLI."""

    def test_fluxo_completo_dry_run(self, pasta_teste, capsys):
        """Testa fluxo completo: main -> dry_run -> saída."""
        result = main([str(pasta_teste), "--dry-run"])
        assert result == 0
        captured = capsys.readouterr()
        assert "PRÉVIA" in captured.out
        assert "Total:" in captured.out

    def test_argumento_posicional_opcional(self, capsys, pasta_vazia):
        """Testa que pasta é opcional (usa Downloads como padrão)."""
        with patch("organizador.core.obter_pasta_downloads", return_value=pasta_vazia):
            with patch("organizador.cli.executar_dry_run", return_value=0) as mock_dry:
                result = main(["--dry-run"])
                assert result == 0
                mock_dry.assert_called_once()
