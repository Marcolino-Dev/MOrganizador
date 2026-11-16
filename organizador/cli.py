"""
Interface de Linha de Comando (CLI) do Organizador Automático de Arquivos.
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import __version__
from .core import (
    Categoria,
    OrganizadorError,
    PastaInvalidaError,
    PermissaoError,
    escanear_pasta,
    executar_organizacao,
    formatar_tamanho,
    obter_pasta_downloads,
    remover_historico,
    salvar_historico,
)

# Configuração de logging
logger = logging.getLogger(__name__)

try:
    from colorama import Fore, Style, init

    init(autoreset=True)
    COLORAMA_AVAILABLE = True
except ImportError:

    class _ColoramaFallback:
        GREEN = YELLOW = RED = CYAN = MAGENTA = BLUE = WHITE = ""
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

    Fore = _ColoramaFallback
    Style = _ColoramaFallback
    COLORAMA_AVAILABLE = False


def criar_parser() -> argparse.ArgumentParser:
    """Cria e configura o parser de argumentos da linha de comando."""
    pasta_padrao = obter_pasta_downloads()

    parser = argparse.ArgumentParser(
        prog="organizer",
        description="Organizador Automático de Arquivos - Agrupa arquivos em pastas por categoria",
        epilog=(
            "Exemplos:\n"
            "  organizer                    # Organiza pasta Downloads\n"
            "  organizer /caminho/pasta     # Organiza pasta específica\n"
            "  organizer -r                 # Organiza e renomeia com data\n"
            "  organizer --dry-run          # Simula sem mover arquivos\n"
            "  organizer --list-categories  # Lista categorias e extensões\n"
            "  organizer --undo             # Desfaz última organização"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "pasta",
        nargs="?",
        default=str(pasta_padrao),
        help=f"Caminho da pasta a organizar (padrão: {pasta_padrao})",
    )

    parser.add_argument(
        "-r",
        "--renomear",
        action="store_true",
        help="Renomeia arquivos adicionando prefixo com data de criação (AAAA-MM-DD_)",
    )

    parser.add_argument(
        "--dry-run",
        "--preview",
        action="store_true",
        help="Simula a organização sem mover arquivos (preview)",
    )

    parser.add_argument(
        "--list-categories", action="store_true", help="Lista todas as categorias e suas extensões"
    )

    parser.add_argument("--undo", action="store_true", help="Desfaz a última organização realizada")

    parser.add_argument(
        "--clear-history", action="store_true", help="Remove o histórico de desfazer salvo"
    )

    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {__version__}")

    parser.add_argument("--verbose", action="store_true", help="Saída verbosa com mais detalhes")

    return parser


def imprimir_cabecalho() -> None:
    """Imprime cabeçalho estilizado."""
    linha = "=" * 60
    print(f"{Fore.MAGENTA}{linha}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}  ORGANIZADOR AUTOMÁTICO DE ARQUIVOS v{__version__}{Style.RESET_ALL}")
    print(f"{Fore.MAGENTA}{linha}{Style.RESET_ALL}")


def listar_categorias() -> None:
    """Lista todas as categorias e suas extensões."""
    from .core import obter_extensoes_categoria

    print(f"\n{Fore.CYAN}CATEGORIAS SUPORTADAS:{Style.RESET_ALL}\n")

    for categoria in Categoria:
        extensoes = obter_extensoes_categoria(categoria)
        print(f"  {categoria.icone}  {Fore.WHITE}{categoria.value}{Style.RESET_ALL}")
        print(f"      Extensões: {', '.join(sorted(extensoes))}")
        print()


def executar_dry_run(pasta: Path, renomear: bool, verbose: bool) -> int:
    """Executa modo preview (dry-run)."""
    movimentos = escanear_pasta(pasta, renomear)

    if not movimentos:
        print(f"{Fore.YELLOW}Nenhum arquivo encontrado para organizar.{Style.RESET_ALL}")
        return 0

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}PRÉVIA (DRY-RUN) - {pasta}{Style.RESET_ALL}")
    if renomear:
        print(f"{Fore.CYAN}Renomeação: ATIVADA (prefixo AAAA-MM-DD_){Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    # Agrupa por categoria para exibição
    por_categoria: Dict[str, List[Dict[str, Any]]] = {}
    for m in movimentos:
        cat = m["categoria"]
        if cat not in por_categoria:
            por_categoria[cat] = []
        por_categoria[cat].append(m)

    total = 0
    for categoria, items in sorted(por_categoria.items()):
        cat_enum = items[0]["categoria_enum"]
        print(
            f"  {cat_enum.icone}  {Fore.WHITE}{categoria}{Style.RESET_ALL} ({len(items)} arquivo(s))"
        )
        for m in items:
            if verbose:
                tamanho = formatar_tamanho(m["tamanho"])
                print(f"    {m['arquivo']} -> {m['novo_nome']} [ {tamanho} ]")
            else:
                print(f"    {m['arquivo']} -> {m['novo_nome']}")
        total += len(items)
        print()

    print(f"  {Fore.CYAN}Total:{Style.RESET_ALL} {total} arquivo(s) seriam movidos")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    return 0


def main(args: Optional[List[str]] = None) -> int:
    """
    Função principal da CLI.

    Args:
        args: Argumentos da linha de comando (None = sys.argv[1:])

    Returns:
        int: Código de saída (0 = sucesso, 1 = erro)
    """
    parser = criar_parser()
    parsed_args = parser.parse_args(args)

    # Comandos especiais que não precisam de pasta válida
    if parsed_args.list_categories:
        listar_categorias()
        return 0

    if parsed_args.undo:
        return executar_desfazer(verbose=parsed_args.verbose)

    if parsed_args.clear_history:
        return executar_limpar_historico()

    pasta = Path(parsed_args.pasta).expanduser().resolve()

    imprimir_cabecalho()

    # Valida pasta
    if not pasta.exists():
        print(f"{Fore.RED}Erro: Pasta não encontrada: {pasta}{Style.RESET_ALL}")
        return 1

    if not pasta.is_dir():
        print(f"{Fore.RED}Erro: Caminho não é uma pasta: {pasta}{Style.RESET_ALL}")
        return 1

    renomear = parsed_args.renomear
    dry_run = parsed_args.dry_run
    verbose = parsed_args.verbose

    if dry_run:
        return executar_dry_run(pasta, renomear, verbose)

    # Execução real
    try:
        print(f"\n{Fore.CYAN}Organizando: {pasta}{Style.RESET_ALL}")
        if renomear:
            print(f"{Fore.CYAN}Renomeação: ATIVADA{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

        def callback(atual, total, arquivo, categoria, novo_nome):
            pct = (atual / total) * 100 if total > 0 else 0
            barra = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            print(f"\r  [{barra}] {pct:5.1f}% | {arquivo[:50]:<50}", end="", flush=True)

        historico = executar_organizacao(pasta, renomear, callback)
        print()  # Nova linha após barra de progresso

        # Salva histórico de forma segura
        try:
            arquivo_hist = salvar_historico(historico)
            logger.info(f"Histórico salvo em {arquivo_hist}")
        except Exception as e:
            logger.warning(f"Não foi possível salvar histórico: {e}")

        # Relatório final
        print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}RELATÓRIO FINAL{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")

        if historico.total_arquivos == 0:
            print(f"{Fore.YELLOW}Nenhum arquivo foi movido.{Style.RESET_ALL}")
        else:
            for categoria in Categoria:
                count = sum(1 for m in historico.movimentos if m.categoria == categoria.value)
                if count > 0:
                    print(f"  {categoria.icone}  {categoria.value}: {count} arquivo(s)")

            print(
                f"\n  {Fore.CYAN}Total movido:{Style.RESET_ALL} {historico.total_arquivos} arquivo(s)"
            )

        if historico.movimentos:
            print(f"\n  {Fore.GREEN}✓ Histórico salvo em local seguro{Style.RESET_ALL}")

        print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

        return 0

    except PastaInvalidaError as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        return 1
    except PermissaoError as e:
        print(f"{Fore.RED}Erro de permissão: {e}{Style.RESET_ALL}")
        print(
            f"{Fore.YELLOW}Dica: Feche programas usando os arquivos ou execute como Administrador.{Style.RESET_ALL}"
        )
        return 1
    except OrganizadorError as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        return 1
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operação cancelada pelo usuário.{Style.RESET_ALL}")
        return 130
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
        if verbose:
            import traceback

            traceback.print_exc()
        return 1


def executar_desfazer(verbose: bool = False) -> int:
    """Executa desfazer da última organização."""
    from .core import OrganizadorError, carregar_historico, desfazer_organizacao

    historico = carregar_historico()
    if not historico or not historico.movimentos:
        print(f"{Fore.YELLOW}Nenhum histórico para desfazer.{Style.RESET_ALL}")
        return 1

    print(f"\n{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}DESFAZENDO ORGANIZAÇÃO{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}")
    print(f"Pasta: {historico.pasta_base}")
    print(f"Arquivos: {historico.total_arquivos}")
    print(f"{Fore.CYAN}{'=' * 60}{Style.RESET_ALL}\n")

    try:

        def callback(atual, total, arquivo, acao, novo_nome):
            pct = (atual / total) * 100 if total > 0 else 0
            barra = "█" * int(pct / 2) + "░" * (50 - int(pct / 2))
            print(f"\r  [{barra}] {pct:5.1f}% | {arquivo[:50]:<50}", end="", flush=True)

        sucessos, erros = desfazer_organizacao(historico, callback)
        print()  # Nova linha

        if erros:
            print(
                f"\n{Fore.YELLOW}Desfeito parcialmente: {sucessos} restaurado(s), {len(erros)} erro(s){Style.RESET_ALL}"
            )
            for erro in erros[:5]:
                print(f"  {Fore.RED}✗{Style.RESET_ALL} {erro}")
            if len(erros) > 5:
                print(f"  ... e mais {len(erros) - 5} erros")
        else:
            print(
                f"\n{Fore.GREEN}✓ Desfeito com sucesso! {sucessos} arquivo(s) restaurado(s){Style.RESET_ALL}"
            )
            remover_historico()

        return 0 if not erros else 1

    except OrganizadorError as e:
        print(f"{Fore.RED}Erro: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Erro inesperado: {e}{Style.RESET_ALL}")
        if verbose:
            import traceback

            traceback.print_exc()
        return 1


def executar_limpar_historico() -> int:
    """Remove histórico de desfazer."""
    if remover_historico():
        print(f"{Fore.GREEN}✓ Histórico removido{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}Nenhum histórico para remover{Style.RESET_ALL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
