"""
Organizador Automático de Arquivos

Um utilitário para organizar arquivos em pastas categorizadas baseado em extensões.
Suporta interface de linha de comando (CLI) e interface gráfica (GUI).
"""

__version__ = "1.0.0"
__author__ = "lairm"
__license__ = "MIT"

from .core import (
    EXTENSOES_CATEGORIAS,
    Categoria,
    HistoricoOrganizacao,
    MovimentoArquivo,
    OrganizadorError,
    PastaInvalidaError,
    PermissaoError,
    carregar_historico,
    desfazer_organizacao,
    escanear_pasta,
    executar_organizacao,
    formatar_tamanho,
    gerar_nome_unico,
    obter_categoria,
    obter_data_criacao,
    obter_pasta_downloads,
    remover_historico,
    salvar_historico,
    validar_pasta,
)

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "Categoria",
    "MovimentoArquivo",
    "HistoricoOrganizacao",
    "EXTENSOES_CATEGORIAS",
    "obter_pasta_downloads",
    "obter_categoria",
    "obter_data_criacao",
    "gerar_nome_unico",
    "escanear_pasta",
    "executar_organizacao",
    "desfazer_organizacao",
    "salvar_historico",
    "carregar_historico",
    "remover_historico",
    "validar_pasta",
    "formatar_tamanho",
    "OrganizadorError",
    "PastaInvalidaError",
    "PermissaoError",
]
