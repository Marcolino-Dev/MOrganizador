"""
Configuração compartilhada para testes pytest.
"""

import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.fixture
def pasta_teste():
    """Cria pasta temporária com arquivos de teste variados."""
    temp_dir = Path(tempfile.mkdtemp(prefix="organizador_test_"))

    # Cria arquivos de teste para cada categoria
    arquivos = {
        # Documentos
        "relatorio.pdf": b"PDF content",
        "documento.docx": b"DOCX content",
        "notas.txt": b"TXT content",
        "planilha.xlsx": b"XLSX content",
        "apresentacao.pptx": b"PPTX content",
        "dados.csv": b"CSV content",
        # Imagens
        "foto.jpg": b"JPG content",
        "imagem.png": b"PNG content",
        "animacao.gif": b"GIF content",
        "vetor.svg": b"SVG content",
        "webp_img.webp": b"WEBP content",
        # Instaladores
        "setup.exe": b"EXE content",
        "instalador.msi": b"MSI content",
        "macos.dmg": b"DMG content",
        "linux.deb": b"DEB content",
        "rpm_pkg.rpm": b"RPM content",
        # Compactados
        "backup.zip": b"ZIP content",
        "arquivo.rar": b"RAR content",
        "tarball.tar": b"TAR content",
        "gzipped.gz": b"GZ content",
        "sevenzip.7z": b"7Z content",
        # Outros
        "desconhecido.xyz": b"XYZ content",
        "script.py": b"PY content",
        "config.json": b"JSON content",
        "readme.md": b"MD content",
    }

    for nome, conteudo in arquivos.items():
        (temp_dir / nome).write_bytes(conteudo)

    yield temp_dir

    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def pasta_vazia():
    """Cria pasta temporária vazia."""
    temp_dir = Path(tempfile.mkdtemp(prefix="organizador_empty_"))
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def pasta_com_subpastas():
    """Cria pasta com subpastas (que devem ser ignoradas)."""
    temp_dir = Path(tempfile.mkdtemp(prefix="organizador_sub_"))

    # Arquivos na raiz
    (temp_dir / "arquivo.txt").write_text("conteudo")
    (temp_dir / "imagem.png").write_bytes(b"png")

    # Subpasta (deve ser ignorada)
    subpasta = temp_dir / "subpasta"
    subpasta.mkdir()
    (subpasta / "dentro.txt").write_text("ignorado")

    # Arquivo oculto (deve ser ignorado)
    (temp_dir / ".oculto").write_text("ignorado")

    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_historico(pasta_teste):
    """Cria um histórico de teste."""
    from organizador.core import HistoricoOrganizacao, MovimentoArquivo

    movimentos = [
        MovimentoArquivo(
            origem=str(pasta_teste / "teste.txt"),
            destino=str(pasta_teste / "Documentos" / "2026-01-01_teste.txt"),
            categoria="Documentos",
        ),
        MovimentoArquivo(
            origem=str(pasta_teste / "foto.jpg"),
            destino=str(pasta_teste / "Imagens" / "2026-01-01_foto.jpg"),
            categoria="Imagens",
        ),
    ]

    return HistoricoOrganizacao(
        timestamp="2026-01-01T12:00:00",
        pasta_base=str(pasta_teste),
        renomear=True,
        movimentos=movimentos,
    )
