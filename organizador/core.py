"""
Módulo core do Organizador Automático de Arquivos.

Contém toda a lógica de negócio compartilhada entre CLI e GUI:
- Categorização de arquivos
- Renomeação com data
- Movimentação e desfazimento
- Histórico persistente
"""

from __future__ import annotations

import json
import logging
import os
import shutil
import sys
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Set, Tuple

# Configuração de logging
logger = logging.getLogger(__name__)

# Constantes de segurança
MAX_PATH_LENGTH = 260 if sys.platform == "win32" else 4096
HISTORICO_FILENAME = ".organizador_historico.json"


def _caminho_seguro(base: Path, destino: Path) -> bool:
    """
    Verifica se o destino está dentro da pasta base (proteção path traversal).

    Args:
        base: Pasta base permitida.
        destino: Caminho a verificar.

    Returns:
        bool: True se destino está dentro de base.
    """
    try:
        base_resolvido = base.resolve(strict=False)
        destino_resolvido = destino.resolve(strict=False)
        # Verifica se destino é subpasta de base
        return base_resolvido in destino_resolvido.parents or base_resolvido == destino_resolvido
    except Exception:
        return False


def _validar_nome_arquivo(nome: str) -> bool:
    """
    Valida se nome de arquivo não contém caracteres perigosos.

    Args:
        nome: Nome do arquivo.

    Returns:
        bool: True se seguro.
    """
    if not nome or len(nome) > 255:
        return False

    # Caracteres perigosos para path traversal
    perigosos = ["..", "~", "$", "`", "|", ";", "&", "<", ">"]
    for p in perigosos:
        if p in nome:
            return False

    # Nomes reservados Windows
    reservados = {
        "CON",
        "PRN",
        "AUX",
        "NUL",
        "COM1",
        "COM2",
        "COM3",
        "COM4",
        "COM5",
        "COM6",
        "COM7",
        "COM8",
        "COM9",
        "LPT1",
        "LPT2",
        "LPT3",
        "LPT4",
        "LPT5",
        "LPT6",
        "LPT7",
        "LPT8",
        "LPT9",
    }
    nome_base = nome.split(".")[0].upper()
    if nome_base in reservados:
        return False

    return True


def _obter_diretorio_historico() -> Path:
    """
    Retorna diretório seguro para arquivo de histórico.
    Usa pasta de dados do usuário (APPDATA no Windows, ~/.local/share no Linux).

    Returns:
        Path: Diretório para histórico.
    """
    if sys.platform == "win32":
        base = Path(os.environ.get("LOCALAPPDATA", os.environ.get("APPDATA", Path.home())))
    else:
        base = Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share"))

    dir_historico = base / "organizador-arquivos"
    dir_historico.mkdir(parents=True, exist_ok=True)
    return dir_historico


def _arquivo_historico() -> Path:
    """Retorna caminho completo do arquivo de histórico."""
    return _obter_diretorio_historico() / HISTORICO_FILENAME


class Categoria(Enum):
    """Enumeração das categorias de arquivos suportadas."""

    DOCUMENTOS = "Documentos"
    IMAGENS = "Imagens"
    INSTALADORES = "Instaladores e Executáveis"
    COMPACTADOS = "Compactados"
    OUTROS = "Outros"

    @property
    def icone(self) -> str:
        """Retorna emoji representativo da categoria."""
        icones = {
            Categoria.DOCUMENTOS: "📄",
            Categoria.IMAGENS: "🖼️",
            Categoria.INSTALADORES: "⚙️",
            Categoria.COMPACTADOS: "🗜️",
            Categoria.OUTROS: "📁",
        }
        return icones.get(self, "📁")

    @property
    def cor_hex(self) -> str:
        """Retorna cor hex para UI."""
        cores = {
            Categoria.DOCUMENTOS: "#3498db",  # Azul
            Categoria.IMAGENS: "#f39c12",  # Laranja
            Categoria.INSTALADORES: "#e74c3c",  # Vermelho
            Categoria.COMPACTADOS: "#27ae60",  # Verde
            Categoria.OUTROS: "#95a5a6",  # Cinza
        }
        return cores.get(self, "#95a5a6")

    @property
    def cor_bg_clara(self) -> str:
        """Retorna cor de fundo clara para tabelas."""
        cores = {
            Categoria.DOCUMENTOS: "#e8f4fd",
            Categoria.IMAGENS: "#fdf2e8",
            Categoria.INSTALADORES: "#fef0f0",
            Categoria.COMPACTADOS: "#f0fdf4",
            Categoria.OUTROS: "#f8f9fa",
        }
        return cores.get(self, "#f8f9fa")


# Mapeamento de extensões para categorias
# Ordem importa: mais específicas primeiro
EXTENSOES_CATEGORIAS: Dict[str, Categoria] = {
    # Documentos
    ".pdf": Categoria.DOCUMENTOS,
    ".docx": Categoria.DOCUMENTOS,
    ".doc": Categoria.DOCUMENTOS,
    ".txt": Categoria.DOCUMENTOS,
    ".xlsx": Categoria.DOCUMENTOS,
    ".xls": Categoria.DOCUMENTOS,
    ".pptx": Categoria.DOCUMENTOS,
    ".ppt": Categoria.DOCUMENTOS,
    ".csv": Categoria.DOCUMENTOS,
    ".ods": Categoria.DOCUMENTOS,
    ".odt": Categoria.DOCUMENTOS,
    ".odp": Categoria.DOCUMENTOS,
    ".rtf": Categoria.DOCUMENTOS,
    ".md": Categoria.DOCUMENTOS,
    ".tex": Categoria.DOCUMENTOS,
    # Imagens
    ".jpg": Categoria.IMAGENS,
    ".jpeg": Categoria.IMAGENS,
    ".png": Categoria.IMAGENS,
    ".gif": Categoria.IMAGENS,
    ".svg": Categoria.IMAGENS,
    ".webp": Categoria.IMAGENS,
    ".bmp": Categoria.IMAGENS,
    ".tiff": Categoria.IMAGENS,
    ".tif": Categoria.IMAGENS,
    ".ico": Categoria.IMAGENS,
    ".heic": Categoria.IMAGENS,
    ".heif": Categoria.IMAGENS,
    ".avif": Categoria.IMAGENS,
    # Instaladores e Executáveis
    ".exe": Categoria.INSTALADORES,
    ".msi": Categoria.INSTALADORES,
    ".dmg": Categoria.INSTALADORES,
    ".pkg": Categoria.INSTALADORES,
    ".deb": Categoria.INSTALADORES,
    ".rpm": Categoria.INSTALADORES,
    ".appimage": Categoria.INSTALADORES,
    ".snap": Categoria.INSTALADORES,
    ".flatpak": Categoria.INSTALADORES,
    ".apk": Categoria.INSTALADORES,
    ".ipa": Categoria.INSTALADORES,
    # Compactados
    ".zip": Categoria.COMPACTADOS,
    ".rar": Categoria.COMPACTADOS,
    ".tar": Categoria.COMPACTADOS,
    ".gz": Categoria.COMPACTADOS,
    ".7z": Categoria.COMPACTADOS,
    ".bz2": Categoria.COMPACTADOS,
    ".xz": Categoria.COMPACTADOS,
    ".zst": Categoria.COMPACTADOS,
    ".tgz": Categoria.COMPACTADOS,
    ".tbz2": Categoria.COMPACTADOS,
    ".txz": Categoria.COMPACTADOS,
}


@dataclass(slots=True)  # type: ignore[call-overload]
class MovimentoArquivo:
    """Registra um movimento de arquivo para possibilitar desfazer."""

    origem: str
    destino: str
    categoria: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "MovimentoArquivo":
        return cls(**data)


@dataclass(slots=True)  # type: ignore[call-overload]
class HistoricoOrganizacao:
    """Histórico completo de uma organização para desfazer."""

    timestamp: str
    pasta_base: str
    renomear: bool
    movimentos: List[MovimentoArquivo] = field(default_factory=list)
    versao: str = "1.0"

    def to_dict(self) -> dict[str, Any]:
        return {
            "versao": self.versao,
            "timestamp": self.timestamp,
            "pasta_base": self.pasta_base,
            "renomear": self.renomear,
            "movimentos": [m.to_dict() for m in self.movimentos],
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "HistoricoOrganizacao":
        movimentos = [MovimentoArquivo.from_dict(m) for m in data.get("movimentos", [])]
        return cls(
            timestamp=data["timestamp"],
            pasta_base=data["pasta_base"],
            renomear=data["renomear"],
            movimentos=movimentos,
            versao=data.get("versao", "1.0"),
        )

    @property
    def total_arquivos(self) -> int:
        return len(self.movimentos)

    @property
    def categorias_unicas(self) -> Set[str]:
        return {m.categoria for m in self.movimentos}


class OrganizadorError(Exception):
    """Exceção base para erros do organizador."""

    pass


class PastaInvalidaError(OrganizadorError):
    """Erro quando pasta não existe ou não é diretório."""

    pass


class PermissaoError(OrganizadorError):
    """Erro de permissão ao acessar/mover arquivos."""

    pass


def obter_pasta_downloads() -> Path:
    """
    Retorna o caminho padrão da pasta Downloads do usuário.

    Returns:
        Path: Caminho para a pasta Downloads ou diretório atual como fallback.
    """
    if sys.platform == "win32":
        downloads = Path(os.environ.get("USERPROFILE", "")) / "Downloads"
    else:
        downloads = Path(os.environ.get("HOME", "")) / "Downloads"

    if downloads.exists() and downloads.is_dir():
        return downloads
    logger.warning("Pasta Downloads não encontrada, usando diretório atual")
    return Path.cwd()


def obter_categoria(extensao: str) -> Categoria:
    """
    Determina a categoria de um arquivo baseado em sua extensão.

    Args:
        extensao: Extensão do arquivo (ex: '.pdf').

    Returns:
        Categoria: Categoria correspondente à extensão ou OUTROS.
    """
    return EXTENSOES_CATEGORIAS.get(extensao.lower(), Categoria.OUTROS)


def obter_data_criacao(arquivo: Path) -> str:
    """
    Obtém a data de criação do arquivo formatada como AAAA-MM-DD.

    No Windows, st_ctime é data de criação.
    No Unix/Linux, st_ctime é última mudança de metadata (fallback para mtime).

    Args:
        arquivo: Caminho do arquivo.

    Returns:
        str: Data formatada (YYYY-MM-DD).
    """
    try:
        stat = arquivo.stat()
        # Tenta tempo de criação (Windows) ou mtime (Unix fallback)
        timestamp = getattr(stat, "st_birthtime", stat.st_mtime)
        return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    except (OSError, AttributeError) as e:
        logger.warning(f"Não foi possível obter data de {arquivo}: {e}")
        return datetime.now().strftime("%Y-%m-%d")


def gerar_nome_unico(destino: Path, nome_base: str, extensao: str) -> Path:
    """
    Gera um nome de arquivo único no destino, adicionando sufixo numérico se necessário.

    Args:
        destino: Pasta de destino.
        nome_base: Nome base do arquivo (sem extensão).
        extensao: Extensão do arquivo (com ponto).

    Returns:
        Path: Caminho completo com nome único garantido.
    """
    contador = 1
    nome_final = f"{nome_base}{extensao}"
    caminho_final = destino / nome_final

    while caminho_final.exists():
        nome_final = f"{nome_base}_{contador}{extensao}"
        caminho_final = destino / nome_final
        contador += 1

    return caminho_final


def _listar_arquivos(pasta: Path) -> List[Path]:
    """
    Lista arquivos regulares (não diretórios, não ocultos) na pasta.

    Args:
        pasta: Caminho da pasta.

    Returns:
        List[Path]: Lista de arquivos ordenados alfabeticamente.
    """
    if not pasta.exists() or not pasta.is_dir():
        return []

    arquivos = [f for f in pasta.iterdir() if f.is_file() and not f.name.startswith(".")]
    return sorted(arquivos, key=lambda x: x.name.lower())


def escanear_pasta(pasta: Path, renomear: bool = False) -> List[Dict[str, Any]]:
    """
    Escaneia a pasta e retorna lista de movimentos planejados (preview).
    Não move arquivos, apenas simula.

    Args:
        pasta: Caminho da pasta a escanear.
        renomear: Se True, inclui prefixo de data no nome.

    Returns:
        List[Dict]: Lista de dicionários com info de cada arquivo.
    """
    movimentos = []
    arquivos = _listar_arquivos(pasta)

    for arquivo in arquivos:
        extensao = arquivo.suffix.lower()
        categoria = obter_categoria(extensao)
        pasta_categoria = pasta / categoria.value

        if renomear:
            data_prefixo = obter_data_criacao(arquivo)
            nome_base = f"{data_prefixo}_{arquivo.stem}"
        else:
            nome_base = arquivo.stem

        destino_final = gerar_nome_unico(pasta_categoria, nome_base, extensao)

        movimentos.append(
            {
                "arquivo": arquivo.name,
                "categoria": categoria.value,
                "categoria_enum": categoria,
                "origem": str(arquivo),
                "destino": str(destino_final),
                "novo_nome": destino_final.name,
                "extensao": extensao,
                "tamanho": arquivo.stat().st_size if arquivo.exists() else 0,
            }
        )

    return movimentos


def executar_organizacao(
    pasta: Path,
    renomear: bool = False,
    callback_progresso: Optional[Callable[[int, int, str, str, str], None]] = None,
) -> HistoricoOrganizacao:
    """
    Executa a organização real dos arquivos e retorna histórico para desfazer.

    Args:
        pasta: Caminho da pasta a organizar.
        renomear: Se True, adiciona prefixo com data de criação.
        callback_progresso: Função chamada a cada arquivo processado
            com args (atual, total, arquivo_original, categoria, novo_nome).

    Returns:
        HistoricoOrganizacao: Histórico completo da operação.

    Raises:
        PastaInvalidaError: Se pasta não existe ou não é diretório.
        PermissaoError: Se sem permissão para mover arquivos.
        OrganizadorError: Se houver tentativa de path traversal.
    """
    # Validação de segurança da pasta
    valido, erro = validar_pasta(pasta)
    if not valido:
        raise PastaInvalidaError(erro)

    # Resolve caminho absoluto para evitar path traversal
    pasta_resolvida = pasta.resolve()

    historico = HistoricoOrganizacao(
        timestamp=datetime.now().isoformat(),
        pasta_base=str(pasta_resolvida),
        renomear=renomear,
    )

    arquivos = _listar_arquivos(pasta_resolvida)
    total = len(arquivos)

    for i, arquivo in enumerate(arquivos):
        try:
            # Validação de segurança do arquivo
            if not _validar_nome_arquivo(arquivo.name):
                logger.warning(f"Ignorando arquivo com nome inseguro: {arquivo.name}")
                continue

            # Verifica se não é symlink (proteção contra link attacks)
            if arquivo.is_symlink():
                logger.warning(f"Ignorando link simbólico: {arquivo.name}")
                continue

            extensao = arquivo.suffix.lower()
            categoria = obter_categoria(extensao)
            pasta_categoria = pasta_resolvida / categoria.value

            # Cria pasta de categoria de forma segura
            try:
                pasta_categoria.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise OrganizadorError(f"Falha ao criar pasta {categoria.value}: {e}") from e

            if renomear:
                data_prefixo = obter_data_criacao(arquivo)
                # Sanitiza nome base
                nome_base = f"{data_prefixo}_{_sanitizar_nome(arquivo.stem)}"
            else:
                nome_base = _sanitizar_nome(arquivo.stem)

            destino_final = gerar_nome_unico(pasta_categoria, nome_base, extensao)

            # Proteção path traversal: garante que destino está dentro da pasta base
            if not _caminho_seguro(pasta_resolvida, destino_final):
                raise OrganizadorError(f"Tentativa de path traversal bloqueada: {destino_final}")

            # Move arquivo de forma atômica onde possível
            shutil.move(str(arquivo), str(destino_final))

            historico.movimentos.append(
                MovimentoArquivo(
                    origem=str(arquivo),
                    destino=str(destino_final),
                    categoria=categoria.value,
                )
            )

            if callback_progresso:
                callback_progresso(i + 1, total, arquivo.name, categoria.value, destino_final.name)

            logger.info(f"Movido: {arquivo.name} -> {categoria.value}/{destino_final.name}")

        except PermissionError as e:
            logger.error(f"Permissão negada para {arquivo.name}: {e}")
            raise PermissaoError(f"Permissão negada: {arquivo.name}") from e
        except shutil.Error as e:
            logger.error(f"Erro ao mover {arquivo.name}: {e}")
            raise OrganizadorError(f"Erro ao mover {arquivo.name}: {e}") from e
        except OSError as e:
            logger.error(f"Erro de sistema ao processar {arquivo.name}: {e}")
            raise OrganizadorError(f"Erro ao processar {arquivo.name}: {e}") from e

    return historico


def _sanitizar_nome(nome: str) -> str:
    """
    Sanitiza nome de arquivo removendo caracteres perigosos.

    Args:
        nome: Nome original.

    Returns:
        str: Nome sanitizado.
    """
    # Remove caracteres de controle e perigosos
    chars_remover = "\x00-\x1f\x7f-\x9f"  # Caracteres de controle
    import re

    nome = re.sub(f"[{re.escape(chars_remover)}]", "", nome)

    # Substitui caracteres problemáticos por underscore
    for c in '<>:"|?*\\/':
        nome = nome.replace(c, "_")

    # Limita tamanho
    if len(nome) > 200:
        nome = nome[:200]

    return nome.strip() or "arquivo"


def desfazer_organizacao(
    historico: HistoricoOrganizacao,
    callback_progresso: Optional[Callable[[int, int, str, str, str], None]] = None,
) -> Tuple[int, List[str]]:
    """
    Desfaz a organização movendo arquivos de volta para a pasta original.

    Args:
        historico: Histórico da organização a desfazer.
        callback_progresso: Função chamada a cada arquivo restaurado
            com args (atual, total, arquivo_atual, acao, novo_nome).

    Returns:
        tuple: (sucessos, lista_erros)
    """
    pasta_base = Path(historico.pasta_base).resolve()
    sucessos = 0
    erros = []

    total = len(historico.movimentos)

    for i, mov in enumerate(historico.movimentos):
        try:
            destino_atual = Path(mov.destino).resolve()
            origem_original = Path(mov.origem).resolve()

            # Proteção path traversal: verifica se ambos estão dentro da pasta base
            if not _caminho_seguro(pasta_base, destino_atual):
                erros.append(f"Path traversal bloqueado no destino: {mov.destino}")
                continue
            if not _caminho_seguro(pasta_base, origem_original):
                erros.append(f"Path traversal bloqueado na origem: {mov.origem}")
                continue

            if not destino_atual.exists():
                erros.append(f"Arquivo não encontrado: {mov.destino}")
                continue

            # Verifica se não é symlink
            if destino_atual.is_symlink():
                erros.append(f"Link simbólico ignorado: {mov.destino}")
                continue

            # Garante que a pasta de origem existe
            try:
                origem_original.parent.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                erros.append(f"Falha ao criar pasta de origem: {e}")
                continue

            # Se já existe arquivo na origem, gera nome único
            if origem_original.exists():
                contador = 1
                nome_base = _sanitizar_nome(origem_original.stem)
                extensao = origem_original.suffix
                while origem_original.exists():
                    origem_original = origem_original.parent / f"{nome_base}_{contador}{extensao}"
                    contador += 1

            # Proteção path traversal no destino final
            if not _caminho_seguro(pasta_base, origem_original):
                erros.append(f"Path traversal bloqueado ao restaurar: {origem_original}")
                continue

            shutil.move(str(destino_atual), str(origem_original))
            sucessos += 1

            if callback_progresso:
                callback_progresso(
                    i + 1, total, destino_atual.name, "↩ Restaurado", origem_original.name
                )

            logger.info(f"Restaurado: {destino_atual.name} -> {origem_original.name}")

        except Exception as e:
            erro_msg = f"Erro ao desfazer {mov.destino}: {e}"
            logger.error(erro_msg)
            erros.append(erro_msg)

    # Remove pastas vazias criadas (apenas se estiverem dentro da pasta base)
    for categoria in Categoria:
        pasta_cat = (pasta_base / categoria.value).resolve()
        if _caminho_seguro(pasta_base, pasta_cat) and pasta_cat.exists() and pasta_cat.is_dir():
            try:
                if not any(pasta_cat.iterdir()):
                    pasta_cat.rmdir()
                    logger.info(f"Pasta vazia removida: {pasta_cat}")
            except Exception as e:
                logger.warning(f"Não foi possível remover pasta {pasta_cat}: {e}")

    return sucessos, erros


def salvar_historico(historico: HistoricoOrganizacao) -> Path:
    """
    Salva histórico em arquivo JSON no diretório seguro do usuário.

    Args:
        historico: Objeto histórico a salvar.

    Returns:
        Path: Caminho do arquivo salvo.
    """
    arquivo = _arquivo_historico()
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(historico.to_dict(), f, ensure_ascii=False, indent=2)
        logger.debug(f"Histórico salvo em {arquivo}")
        return arquivo
    except Exception as e:
        logger.error(f"Falha ao salvar histórico: {e}")
        raise OrganizadorError(f"Falha ao salvar histórico: {e}") from e


def carregar_historico() -> Optional[HistoricoOrganizacao]:
    """
    Carrega histórico do arquivo JSON do diretório seguro.

    Returns:
        HistoricoOrganizacao ou None se falhar.
    """
    arquivo = _arquivo_historico()
    try:
        if not arquivo.exists():
            return None
        with open(arquivo, "r", encoding="utf-8") as f:
            data = json.load(f)
        return HistoricoOrganizacao.from_dict(data)
    except Exception as e:
        logger.warning(f"Falha ao carregar histórico: {e}")
        return None


def remover_historico() -> bool:
    """
    Remove arquivo de histórico.

    Returns:
        bool: True se removido com sucesso.
    """
    arquivo = _arquivo_historico()
    try:
        if arquivo.exists():
            arquivo.unlink()
            logger.info("Histórico removido")
            return True
        return False
    except Exception as e:
        logger.error(f"Falha ao remover histórico: {e}")
        return False


def formatar_tamanho(bytes_: float) -> str:
    """Formata tamanho em bytes para string legível."""
    for unidade in ["B", "KB", "MB", "GB", "TB"]:
        if bytes_ < 1024.0:
            return f"{bytes_:.1f} {unidade}"
        bytes_ /= 1024.0
    return f"{bytes_:.1f} PB"


def obter_extensoes_categoria(categoria: Categoria) -> List[str]:
    """Retorna lista de extensões para uma categoria."""
    return [ext for ext, cat in EXTENSOES_CATEGORIAS.items() if cat == categoria]


def validar_pasta(pasta: Path) -> Tuple[bool, Optional[str]]:
    """
    Valida se uma pasta pode ser organizada.

    Returns:
        tuple: (valido, mensagem_erro)
    """
    if not pasta.exists():
        return False, "Pasta não encontrada"
    if not pasta.is_dir():
        return False, "Caminho não é uma pasta"
    if not os.access(pasta, os.R_OK | os.W_OK):
        return False, "Sem permissão de leitura/escrita na pasta"
    return True, None
