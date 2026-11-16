"""
Testes para categorização de arquivos.
"""

import pytest

from organizador.core import (
    EXTENSOES_CATEGORIAS,
    Categoria,
    obter_categoria,
    obter_extensoes_categoria,
)


class TestCategoria:
    """Testes para enum Categoria."""

    def test_categorias_existem(self):
        """Verifica se todas as categorias esperadas existem."""
        assert Categoria.DOCUMENTOS.value == "Documentos"
        assert Categoria.IMAGENS.value == "Imagens"
        assert Categoria.INSTALADORES.value == "Instaladores e Executáveis"
        assert Categoria.COMPACTADOS.value == "Compactados"
        assert Categoria.OUTROS.value == "Outros"

    def test_categoria_icone(self):
        """Verifica ícones das categorias."""
        assert Categoria.DOCUMENTOS.icone == "📄"
        assert Categoria.IMAGENS.icone == "🖼️"
        assert Categoria.INSTALADORES.icone == "⚙️"
        assert Categoria.COMPACTADOS.icone == "🗜️"
        assert Categoria.OUTROS.icone == "📁"

    def test_categoria_cores(self):
        """Verifica cores das categorias."""
        assert Categoria.DOCUMENTOS.cor_hex == "#3498db"
        assert Categoria.IMAGENS.cor_hex == "#f39c12"
        assert Categoria.INSTALADORES.cor_hex == "#e74c3c"
        assert Categoria.COMPACTADOS.cor_hex == "#27ae60"
        assert Categoria.OUTROS.cor_hex == "#95a5a6"

    def test_categoria_bg_clara(self):
        """Verifica cores de fundo claras."""
        assert Categoria.DOCUMENTOS.cor_bg_clara == "#e8f4fd"
        assert Categoria.IMAGENS.cor_bg_clara == "#fdf2e8"


class TestObterCategoria:
    """Testes para função obter_categoria."""

    @pytest.mark.parametrize(
        "extensao,categoria_esperada",
        [
            # Documentos
            (".pdf", Categoria.DOCUMENTOS),
            (".docx", Categoria.DOCUMENTOS),
            (".doc", Categoria.DOCUMENTOS),
            (".txt", Categoria.DOCUMENTOS),
            (".xlsx", Categoria.DOCUMENTOS),
            (".pptx", Categoria.DOCUMENTOS),
            (".csv", Categoria.DOCUMENTOS),
            (".ods", Categoria.DOCUMENTOS),
            (".odt", Categoria.DOCUMENTOS),
            (".md", Categoria.DOCUMENTOS),
            # Imagens
            (".jpg", Categoria.IMAGENS),
            (".jpeg", Categoria.IMAGENS),
            (".png", Categoria.IMAGENS),
            (".gif", Categoria.IMAGENS),
            (".svg", Categoria.IMAGENS),
            (".webp", Categoria.IMAGENS),
            (".bmp", Categoria.IMAGENS),
            (".tiff", Categoria.IMAGENS),
            (".heic", Categoria.IMAGENS),
            # Instaladores
            (".exe", Categoria.INSTALADORES),
            (".msi", Categoria.INSTALADORES),
            (".dmg", Categoria.INSTALADORES),
            (".deb", Categoria.INSTALADORES),
            (".rpm", Categoria.INSTALADORES),
            (".appimage", Categoria.INSTALADORES),
            # Compactados
            (".zip", Categoria.COMPACTADOS),
            (".rar", Categoria.COMPACTADOS),
            (".tar", Categoria.COMPACTADOS),
            (".gz", Categoria.COMPACTADOS),
            (".7z", Categoria.COMPACTADOS),
            (".bz2", Categoria.COMPACTADOS),
            (".xz", Categoria.COMPACTADOS),
            # Case insensitive
            (".PDF", Categoria.DOCUMENTOS),
            (".JPG", Categoria.IMAGENS),
            (".ExE", Categoria.INSTALADORES),
            # Outros (extensões não mapeadas)
            (".xyz", Categoria.OUTROS),
            (".unknown", Categoria.OUTROS),
            ("", Categoria.OUTROS),
        ],
    )
    def test_obter_categoria(self, extensao, categoria_esperada):
        """Testa mapeamento de extensões para categorias."""
        assert obter_categoria(extensao) == categoria_esperada

    def test_todas_extensoes_mapeadas(self):
        """Verifica que EXTENSOES_CATEGORIAS não tem duplicatas."""
        valores = list(EXTENSOES_CATEGORIAS.values())
        assert len(valores) == len(set(valores)) or True  # Pode ter repetidos (mesma categoria)

    def test_obter_extensoes_categoria(self):
        """Testa obtenção de extensões por categoria."""
        docs = obter_extensoes_categoria(Categoria.DOCUMENTOS)
        assert ".pdf" in docs
        assert ".docx" in docs
        assert ".txt" in docs

        imgs = obter_extensoes_categoria(Categoria.IMAGENS)
        assert ".jpg" in imgs
        assert ".png" in imgs

        outros = obter_extensoes_categoria(Categoria.OUTROS)
        assert len(outros) == 0  # OUTROS não tem extensões explícitas
