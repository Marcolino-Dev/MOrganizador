"""
Testes para funcionalidades core do organizador.
"""

from pathlib import Path

import pytest

from organizador.core import (
    HistoricoOrganizacao,
    MovimentoArquivo,
    PastaInvalidaError,
    _arquivo_historico,
    carregar_historico,
    desfazer_organizacao,
    escanear_pasta,
    executar_organizacao,
    formatar_tamanho,
    gerar_nome_unico,
    obter_data_criacao,
    remover_historico,
    salvar_historico,
    validar_pasta,
)


class TestMovimentoArquivo:
    """Testes para dataclass MovimentoArquivo."""

    def test_criacao(self):
        mov = MovimentoArquivo(
            origem="/origem/arquivo.txt", destino="/destino/arquivo.txt", categoria="Documentos"
        )
        assert mov.origem == "/origem/arquivo.txt"
        assert mov.destino == "/destino/arquivo.txt"
        assert mov.categoria == "Documentos"

    def test_to_dict(self):
        mov = MovimentoArquivo("/a", "/b", "Cat")
        d = mov.to_dict()
        assert d == {"origem": "/a", "destino": "/b", "categoria": "Cat"}

    def test_from_dict(self):
        d = {"origem": "/a", "destino": "/b", "categoria": "Cat"}
        mov = MovimentoArquivo.from_dict(d)
        assert mov.origem == "/a"
        assert mov.destino == "/b"
        assert mov.categoria == "Cat"


class TestHistoricoOrganizacao:
    """Testes para dataclass HistoricoOrganizacao."""

    def test_criacao_basica(self):
        hist = HistoricoOrganizacao(
            timestamp="2026-01-01T12:00:00", pasta_base="/teste", renomear=True
        )
        assert hist.timestamp == "2026-01-01T12:00:00"
        assert hist.pasta_base == "/teste"
        assert hist.renomear is True
        assert hist.movimentos == []
        assert hist.versao == "1.0"

    def test_com_movimentos(self):
        movs = [
            MovimentoArquivo("/a", "/b", "Cat1"),
            MovimentoArquivo("/c", "/d", "Cat2"),
        ]
        hist = HistoricoOrganizacao(
            timestamp="2026-01-01T12:00:00", pasta_base="/teste", renomear=False, movimentos=movs
        )
        assert hist.total_arquivos == 2
        assert hist.categorias_unicas == {"Cat1", "Cat2"}

    def test_serializacao(self):
        movs = [MovimentoArquivo("/a", "/b", "Cat")]
        hist = HistoricoOrganizacao(
            timestamp="2026-01-01T12:00:00", pasta_base="/teste", renomear=True, movimentos=movs
        )
        d = hist.to_dict()
        assert d["versao"] == "1.0"
        assert d["timestamp"] == "2026-01-01T12:00:00"
        assert d["pasta_base"] == "/teste"
        assert d["renomear"] is True
        assert len(d["movimentos"]) == 1

    def test_deserializacao(self):
        d = {
            "versao": "1.0",
            "timestamp": "2026-01-01T12:00:00",
            "pasta_base": "/teste",
            "renomear": True,
            "movimentos": [{"origem": "/a", "destino": "/b", "categoria": "Cat"}],
        }
        hist = HistoricoOrganizacao.from_dict(d)
        assert hist.timestamp == "2026-01-01T12:00:00"
        assert hist.pasta_base == "/teste"
        assert hist.renomear is True
        assert len(hist.movimentos) == 1
        assert hist.movimentos[0].origem == "/a"

    def test_deserializacao_sem_versao(self):
        """Compatibilidade com histórico antigo sem campo versao."""
        d = {
            "timestamp": "2026-01-01T12:00:00",
            "pasta_base": "/teste",
            "renomear": True,
            "movimentos": [],
        }
        hist = HistoricoOrganizacao.from_dict(d)
        assert hist.versao == "1.0"


class TestObterDataCriacao:
    """Testes para obter_data_criacao."""

    def test_arquivo_existente(self, pasta_teste):
        arquivo = pasta_teste / "relatorio.pdf"
        data = obter_data_criacao(arquivo)
        # Formato YYYY-MM-DD
        assert len(data) == 10
        assert data[4] == "-"
        assert data[7] == "-"

    def test_arquivo_inexistente(self):
        data = obter_data_criacao(Path("/nao/existe.txt"))
        # Deve retornar data atual como fallback
        assert len(data) == 10


class TestGerarNomeUnico:
    """Testes para gerar_nome_unico."""

    def test_sem_conflito(self, pasta_teste):
        destino = gerar_nome_unico(pasta_teste, "arquivo", ".txt")
        assert destino.name == "arquivo.txt"
        assert destino.parent == pasta_teste

    def test_com_conflito(self, pasta_teste):
        # Cria arquivo existente
        (pasta_teste / "arquivo.txt").write_text("existente")

        destino = gerar_nome_unico(pasta_teste, "arquivo", ".txt")
        assert destino.name == "arquivo_1.txt"

    def test_multiplos_conflitos(self, pasta_teste):
        # Cria arquivos: arquivo.txt, arquivo_1.txt, arquivo_2.txt
        (pasta_teste / "arquivo.txt").write_text("0")
        (pasta_teste / "arquivo_1.txt").write_text("1")
        (pasta_teste / "arquivo_2.txt").write_text("2")

        destino = gerar_nome_unico(pasta_teste, "arquivo", ".txt")
        assert destino.name == "arquivo_3.txt"

    def test_com_extensao_com_ponto(self, pasta_teste):
        destino = gerar_nome_unico(pasta_teste, "teste", ".pdf")
        assert destino.suffix == ".pdf"

    def test_sem_extensao(self, pasta_teste):
        destino = gerar_nome_unico(pasta_teste, "semext", "")
        assert destino.name == "semext"


class TestEscanearPasta:
    """Testes para escanear_pasta (preview)."""

    def test_retorna_lista_movimentos(self, pasta_teste):
        movimentos = escanear_pasta(pasta_teste, renomear=False)
        assert len(movimentos) > 0
        # Verifica estrutura
        for m in movimentos:
            assert "arquivo" in m
            assert "categoria" in m
            assert "origem" in m
            assert "destino" in m
            assert "novo_nome" in m
            assert "categoria_enum" in m

    def test_renomear_true(self, pasta_teste):
        movimentos = escanear_pasta(pasta_teste, renomear=True)
        for m in movimentos:
            # Novo nome deve começar com data YYYY-MM-DD_
            assert len(m["novo_nome"]) > 11
            assert m["novo_nome"][4] == "-"
            assert m["novo_nome"][7] == "-"
            assert m["novo_nome"][10] == "_"

    def test_renomear_false(self, pasta_teste):
        movimentos = escanear_pasta(pasta_teste, renomear=False)
        for m in movimentos:
            # Novo nome deve ser igual ao original (sem prefixo de data)
            assert m["novo_nome"] == m["arquivo"] or m["novo_nome"].startswith(
                m["arquivo"].split(".")[0]
            )

    def test_pasta_inexistente(self):
        movimentos = escanear_pasta(Path("/nao/existe"), renomear=False)
        assert movimentos == []

    def test_ignora_arquivos_ocultos(self, pasta_com_subpastas):
        movimentos = escanear_pasta(pasta_com_subpastas, renomear=False)
        nomes = [m["arquivo"] for m in movimentos]
        assert ".oculto" not in nomes

    def test_ignora_subpastas(self, pasta_com_subpastas):
        movimentos = escanear_pasta(pasta_com_subpastas, renomear=False)
        nomes = [m["arquivo"] for m in movimentos]
        assert "dentro.txt" not in nomes  # Está em subpasta


class TestExecutarOrganizacao:
    """Testes para executar_organizacao (operação real)."""

    def test_organiza_arquivos(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=False)

        assert historico.total_arquivos > 0
        # Verifica se pastas de categoria foram criadas
        assert (pasta_teste / "Documentos").exists()
        assert (pasta_teste / "Imagens").exists()
        assert (pasta_teste / "Instaladores e Executáveis").exists()
        assert (pasta_teste / "Compactados").exists()
        assert (pasta_teste / "Outros").exists()

        # Verifica se arquivos foram movidos
        for mov in historico.movimentos:
            assert Path(mov.destino).exists()
            assert not Path(mov.origem).exists()

    def test_organiza_com_renomear(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=True)

        assert historico.total_arquivos > 0
        for mov in historico.movimentos:
            # Nome deve ter prefixo de data
            nome = Path(mov.destino).name
            assert len(nome) > 11
            assert nome[4] == "-"
            assert nome[7] == "-"
            assert nome[10] == "_"

    def test_pasta_invalida(self):
        with pytest.raises(PastaInvalidaError):
            executar_organizacao(Path("/nao/existe"))

    def test_callback_progresso(self, pasta_teste):
        chamadas = []

        def callback(atual, total, arquivo, cat, novo):
            chamadas.append((atual, total, arquivo, cat, novo))

        historico = executar_organizacao(pasta_teste, renomear=False, callback_progresso=callback)
        assert len(chamadas) == historico.total_arquivos
        # Verifica ordem
        for i, (atual, total, *_) in enumerate(chamadas):
            assert atual == i + 1
            assert total == historico.total_arquivos

    def test_conflito_nomes_gera_sufixo(self, pasta_teste):
        # Cria pasta temporária limpa para este teste
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            pasta_limpa = Path(tmp)
            # Cria dois arquivos com mesmo nome base mas extensões diferentes
            # que caem na mesma categoria
            (pasta_limpa / "teste.txt").write_text("1")
            (pasta_limpa / "teste.csv").write_text("2")

            historico = executar_organizacao(pasta_limpa, renomear=False)

            # Ambos devem estar em Documentos com nomes únicos
            destinos = [
                Path(m.destino).name for m in historico.movimentos if m.categoria == "Documentos"
            ]
            assert len(destinos) == 2
            assert len(set(destinos)) == 2  # Nomes únicos


class TestDesfazerOrganizacao:
    """Testes para desfazer_organizacao."""

    def test_desfaz_completo(self, pasta_teste):
        # Organiza
        historico = executar_organizacao(pasta_teste, renomear=False)
        total_original = historico.total_arquivos

        # Desfaz
        sucessos, erros = desfazer_organizacao(historico)

        assert sucessos == total_original
        assert len(erros) == 0

        # Verifica se arquivos voltaram
        for mov in historico.movimentos:
            assert Path(mov.origem).exists()
            assert not Path(mov.destino).exists()

    def test_desfaz_com_renomear(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=True)
        sucessos, erros = desfazer_organizacao(historico)

        assert sucessos == historico.total_arquivos
        assert len(erros) == 0

    def test_remove_pastas_vazias(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=False)
        desfazer_organizacao(historico)

        # Pastas de categoria devem ser removidas se vazias
        for cat in ["Documentos", "Imagens", "Instaladores e Executáveis", "Compactados", "Outros"]:
            pasta_cat = pasta_teste / cat
            if pasta_cat.exists():
                assert any(pasta_cat.iterdir()), f"Pasta {cat} não vazia após desfazer"

    def test_arquivo_ja_existente_na_origem(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=False)

        # Recria um arquivo na origem original
        primeiro = historico.movimentos[0]
        Path(primeiro.origem).write_text("novo conteudo")

        sucessos, erros = desfazer_organizacao(historico)
        # Deve ter sucesso (gera nome único)
        assert sucessos == historico.total_arquivos

    def test_arquivo_destino_nao_existe(self, pasta_teste):
        historico = executar_organizacao(pasta_teste, renomear=False)
        # Remove um arquivo do destino manualmente
        Path(historico.movimentos[0].destino).unlink()

        sucessos, erros = desfazer_organizacao(historico)
        assert sucessos == historico.total_arquivos - 1
        assert len(erros) == 1
        assert "não encontrado" in erros[0]


class TestHistoricoPersistencia:
    """Testes para salvar/carregar histórico."""

    def test_salvar_carregar(self, mock_historico):
        arquivo = salvar_historico(mock_historico)
        assert arquivo.exists()

        carregado = carregar_historico()
        assert carregado is not None
        assert carregado.timestamp == mock_historico.timestamp
        assert carregado.pasta_base == mock_historico.pasta_base
        assert carregado.renomear == mock_historico.renomear
        assert len(carregado.movimentos) == len(mock_historico.movimentos)

    def test_carregar_inexistente(self):
        # Remove histórico se existir para testar carregar inexistente
        remover_historico()
        resultado = carregar_historico()
        assert resultado is None

    def test_carregar_corrompido(self):
        # Salva histórico válido primeiro
        from datetime import datetime

        from organizador.core import HistoricoOrganizacao

        historico_valido = HistoricoOrganizacao(
            pasta_base="/tmp/teste",
            movimentos=[],
            renomear=False,
            timestamp=datetime.now().isoformat(),
            versao="1.0",
        )
        salvar_historico(historico_valido)

        # Corrompe o arquivo
        arquivo = _arquivo_historico()
        arquivo.write_text("{json invalido}")

        resultado = carregar_historico()
        assert resultado is None


class TestUtilitarios:
    """Testes para funções utilitárias."""

    def test_formatar_tamanho(self):
        assert formatar_tamanho(500) == "500.0 B"
        assert formatar_tamanho(1024) == "1.0 KB"
        assert formatar_tamanho(1024 * 1024) == "1.0 MB"
        assert formatar_tamanho(1024 * 1024 * 1024) == "1.0 GB"
        assert formatar_tamanho(1024 * 1024 * 1024 * 1024) == "1.0 TB"

    def test_validar_pasta_valida(self, pasta_teste):
        valido, erro = validar_pasta(pasta_teste)
        assert valido is True
        assert erro is None

    def test_validar_pasta_inexistente(self):
        valido, erro = validar_pasta(Path("/nao/existe"))
        assert valido is False
        assert "não encontrada" in erro.lower()

    def test_validar_arquivo_como_pasta(self, pasta_teste):
        arquivo = pasta_teste / "relatorio.pdf"
        valido, erro = validar_pasta(arquivo)
        assert valido is False
        assert "não é uma pasta" in erro.lower()
