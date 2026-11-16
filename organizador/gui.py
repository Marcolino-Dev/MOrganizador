"""
Interface Gráfica (GUI) do Organizador Automático de Arquivos.

Baseada em Tkinter nativo, com design moderno e responsivo.
"""

import logging
import sys
import tkinter as tk
from functools import partial
from pathlib import Path
from threading import Thread
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional

from . import __version__
from .core import (
    Categoria,
    HistoricoOrganizacao,
    OrganizadorError,
    PastaInvalidaError,
    PermissaoError,
    carregar_historico,
    desfazer_organizacao,
    escanear_pasta,
    executar_organizacao,
    obter_pasta_downloads,
    salvar_historico,
)

# Configuração de logging
logger = logging.getLogger(__name__)


class OrganizadorGUI:
    """Interface gráfica principal do Organizador."""

    # Constantes de UI
    LARGURA_MIN = 850
    ALTURA_MIN = 600
    LARGURA_PADRAO = 1000
    ALTURA_PADRAO = 700

    CORES = {
        "primaria": "#2c3e50",
        "secundaria": "#34495e",
        "sucesso": "#27ae60",
        "aviso": "#f39c12",
        "erro": "#e74c3c",
        "info": "#3498db",
        "fundo": "#ecf0f1",
        "branco": "#ffffff",
        "texto": "#2c3e50",
        "texto_claro": "#7f8c8d",
    }

    def __init__(self, root: tk.Tk):
        self.root = root
        self._configurar_janela()
        self._inicializar_variaveis()
        self._carregar_historico_salvo()
        self._criar_interface()
        self._configurar_atalhos()
        self.atualizar_preview()

    def _configurar_janela(self) -> None:
        """Configura propriedades da janela principal."""
        self.root.title(f"Organizador Automático de Arquivos v{__version__}")
        self.root.geometry(f"{self.LARGURA_PADRAO}x{self.ALTURA_PADRAO}")
        self.root.minsize(self.LARGURA_MIN, self.ALTURA_MIN)

        # Centraliza na tela
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.LARGURA_PADRAO // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.ALTURA_PADRAO // 2)
        self.root.geometry(f"+{x}+{y}")

        # Tenta definir ícone
        self._definir_icone()

        # Configura fechamento
        self.root.protocol("WM_DELETE_WINDOW", self._ao_fechar)

    def _definir_icone(self) -> None:
        """Tenta definir ícone da janela."""
        try:
            # Procura ícone em locais possíveis
            base_dir = Path(__file__).parent.parent
            for nome in ["assets/logo.ico", "assets/logo.png", "logo.ico", "logo.png"]:
                icone_path = base_dir / nome
                if icone_path.exists():
                    if nome.endswith(".ico"):
                        self.root.iconbitmap(str(icone_path))
                    else:
                        img = tk.PhotoImage(file=str(icone_path))
                        self.root.iconphoto(True, img)
                    break
        except Exception:
            pass  # Ignora se não conseguir definir ícone

    def _inicializar_variaveis(self) -> None:
        """Inicializa variáveis de estado."""
        self.pasta_selecionada = tk.StringVar(value=str(obter_pasta_downloads()))
        self.renomear_var = tk.BooleanVar(value=True)
        self.movimentos_preview: List[Dict[str, Any]] = []
        self.historico_atual: Optional[HistoricoOrganizacao] = None
        self.arquivo_historico = Path.cwd() / ".organizador_historico.json"
        self.organizando = False
        self._preview_debounce_id: Optional[str] = None

    def _carregar_historico_salvo(self) -> None:
        """Carrega histórico do arquivo JSON se existir."""
        # Nova API segura: carrega do diretório de configuração do usuário
        self.historico_atual = carregar_historico()

    def _criar_interface(self) -> None:
        """Cria toda a interface gráfica."""
        self._configurar_estilos()
        self._criar_layout_principal()

    def _configurar_estilos(self) -> None:
        """Configura estilos personalizados ttk."""
        style = ttk.Style()
        style.theme_use("clam")

        # Configurações de cores
        style.configure(".", background=self.CORES["fundo"], foreground=self.CORES["texto"])
        style.configure("TFrame", background=self.CORES["fundo"])
        style.configure("TLabel", background=self.CORES["fundo"], foreground=self.CORES["texto"])
        style.configure(
            "TLabelFrame", background=self.CORES["fundo"], foreground=self.CORES["primaria"]
        )
        style.configure(
            "TLabelFrame.Label", font=("Segoe UI", 10, "bold"), foreground=self.CORES["primaria"]
        )
        style.configure("TButton", font=("Segoe UI", 10), padding=(12, 6))
        style.configure("TEntry", font=("Segoe UI", 10), padding=6)
        style.configure("TCheckbutton", font=("Segoe UI", 10), background=self.CORES["fundo"])
        style.configure("TPanedwindow", background=self.CORES["fundo"])
        style.configure("TProgressbar", thickness=8)

        # Estilos customizados
        style.configure(
            "Titulo.TLabel", font=("Segoe UI", 18, "bold"), foreground=self.CORES["primaria"]
        )
        style.configure(
            "Subtitulo.TLabel", font=("Segoe UI", 10), foreground=self.CORES["texto_claro"]
        )
        style.configure(
            "Estatisticas.TLabel", font=("Segoe UI", 10, "bold"), foreground=self.CORES["sucesso"]
        )
        style.configure("Aviso.TLabel", font=("Segoe UI", 10), foreground=self.CORES["aviso"])
        style.configure("Erro.TLabel", font=("Segoe UI", 10), foreground=self.CORES["erro"])
        style.configure("Status.TLabel", font=("Segoe UI", 9), foreground=self.CORES["texto_claro"])

        style.configure("Primario.TButton", font=("Segoe UI", 11, "bold"), padding=(20, 10))
        style.configure(
            "Perigo.TButton",
            font=("Segoe UI", 11, "bold"),
            padding=(20, 10),
            foreground=self.CORES["erro"],
        )
        style.configure("Secundario.TButton", font=("Segoe UI", 10), padding=(15, 8))

        # Treeview
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=28)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.map("Treeview", background=[("selected", self.CORES["info"])])

    def _criar_layout_principal(self) -> None:
        """Cria layout principal com frames."""
        # Frame principal com padding
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Configura grid weights
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)  # Preview expande

        # Cabeçalho
        self._criar_cabecalho(main_frame)

        # Seletor de pasta
        self._criar_seletor_pasta(main_frame)

        # Prévia (expande)
        self._criar_preview(main_frame)

        # Barra de progresso
        self._criar_progresso(main_frame)

        # Botões de ação
        self._criar_botoes_acao(main_frame)

    def _criar_cabecalho(self, parent: ttk.Frame) -> None:
        """Cria cabeçalho com título e subtítulo."""
        header = ttk.Frame(parent)
        header.grid(row=0, column=0, sticky="ew", pady=(0, 20))

        ttk.Label(header, text="📁 Organizador Automático de Arquivos", style="Titulo.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="Organize seus arquivos por categoria com um clique",
            style="Subtitulo.TLabel",
        ).pack(anchor=tk.W)

        # Linha separadora
        sep = ttk.Separator(header, orient="horizontal")
        sep.pack(fill=tk.X, pady=(10, 0))

    def _criar_seletor_pasta(self, parent: ttk.Frame) -> None:
        """Cria seção de seleção de pasta."""
        folder_frame = ttk.LabelFrame(parent, text="📂 Pasta a Organizar", padding=15)
        folder_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        folder_frame.columnconfigure(0, weight=1)

        # Campo de entrada + botões
        input_frame = ttk.Frame(folder_frame)
        input_frame.grid(row=0, column=0, sticky="ew")
        input_frame.columnconfigure(0, weight=1)

        self.entry_pasta = ttk.Entry(input_frame, textvariable=self.pasta_selecionada)
        self.entry_pasta.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.entry_pasta.bind("<KeyRelease>", self._ao_alterar_pasta)
        self.entry_pasta.bind("<Return>", lambda e: self.atualizar_preview())

        ttk.Button(
            input_frame,
            text="📁 Procurar",
            command=self.selecionar_pasta,
            style="Secundario.TButton",
        ).grid(row=0, column=1, padx=(0, 5))
        ttk.Button(
            input_frame,
            text="🔄 Atualizar",
            command=self.atualizar_preview,
            style="Secundario.TButton",
        ).grid(row=0, column=2)

        # Opções
        opts_frame = ttk.Frame(folder_frame)
        opts_frame.grid(row=1, column=0, sticky="ew", pady=(12, 0))

        self.chk_renomear = ttk.Checkbutton(
            opts_frame,
            text="✏️ Renomear com data de criação (AAAA-MM-DD_)",
            variable=self.renomear_var,
            command=self._ao_alterar_opcoes,
        )
        self.chk_renomear.pack(side=tk.LEFT)

        # Tooltip para checkbox
        self._criar_tooltip(
            self.chk_renomear,
            "Adiciona prefixo com a data de criação do arquivo\nEx: 2026-11-15_relatorio.pdf",
        )

    def _criar_preview(self, parent: ttk.Frame) -> None:
        """Cria área de prévia com Treeview."""
        preview_frame = ttk.LabelFrame(parent, text="👁️ Prévia da Organização", padding=15)
        preview_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 15))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)

        # Toolbar
        toolbar = ttk.Frame(preview_frame)
        toolbar.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        toolbar.columnconfigure(1, weight=1)

        # Contador/estatísticas
        self.lbl_estatisticas = ttk.Label(
            toolbar, text="Carregando...", style="Estatisticas.TLabel"
        )
        self.lbl_estatisticas.grid(row=0, column=0, sticky="w")

        # Botões da toolbar
        btn_frame = ttk.Frame(toolbar)
        btn_frame.grid(row=0, column=1, sticky="e")

        ttk.Button(
            btn_frame,
            text="⬆ Expandir Tudo",
            command=self._expandir_tudo,
            style="Secundario.TButton",
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame,
            text="⬇ Colapsar Tudo",
            command=self._colapsar_tudo,
            style="Secundario.TButton",
        ).pack(side=tk.LEFT, padx=2)
        ttk.Button(
            btn_frame,
            text="📋 Copiar Lista",
            command=self._copiar_lista,
            style="Secundario.TButton",
        ).pack(side=tk.LEFT, padx=2)

        # Treeview com scrollbars
        tree_frame = ttk.Frame(preview_frame)
        tree_frame.grid(row=1, column=0, sticky="nsew")
        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        columns = ("arquivo", "categoria", "novo_nome", "tamanho")
        self.tree_preview = ttk.Treeview(
            tree_frame, columns=columns, show="headings", height=14, selectmode="extended"
        )

        self.tree_preview.heading(
            "arquivo", text="📄 Arquivo Original", command=lambda: self._ordenar_coluna("arquivo")
        )
        self.tree_preview.heading(
            "categoria", text="📁 Categoria", command=lambda: self._ordenar_coluna("categoria")
        )
        self.tree_preview.heading(
            "novo_nome", text="✨ Novo Nome", command=lambda: self._ordenar_coluna("novo_nome")
        )
        self.tree_preview.heading(
            "tamanho", text="📦 Tamanho", command=lambda: self._ordenar_coluna("tamanho")
        )

        self.tree_preview.column("arquivo", width=350, minwidth=250, anchor=tk.W)
        self.tree_preview.column("categoria", width=200, minwidth=160, anchor=tk.CENTER)
        self.tree_preview.column("novo_nome", width=350, minwidth=250, anchor=tk.W)
        self.tree_preview.column("tamanho", width=100, minwidth=80, anchor=tk.E)

        # Scrollbars
        scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree_preview.yview)
        scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree_preview.xview)
        self.tree_preview.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)

        self.tree_preview.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")

        # Tags para cores por categoria
        for cat in Categoria:
            self.tree_preview.tag_configure(cat.name.lower(), background=cat.cor_bg_clara)

        # Bind events
        self.tree_preview.bind("<Double-1>", self._ao_duplo_clique)
        self.tree_preview.bind("<Key>", self._ao_tecla_tree)

    def _criar_progresso(self, parent: ttk.Frame) -> None:
        """Cria barra de progresso e status."""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame, variable=self.progress_var, maximum=100, mode="determinate"
        )
        self.progress_bar.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        self.lbl_status = ttk.Label(
            progress_frame, text="Pronto para organizar", style="Status.TLabel"
        )
        self.lbl_status.grid(row=1, column=0, sticky="w")

    def _criar_botoes_acao(self, parent: ttk.Frame) -> None:
        """Cria botões de ação principais."""
        btn_frame = ttk.Frame(parent)
        btn_frame.grid(row=4, column=0, sticky="ew")
        btn_frame.columnconfigure(1, weight=1)

        # Botão Iniciar (primário)
        self.btn_iniciar = ttk.Button(
            btn_frame,
            text="🚀 Iniciar Organização",
            style="Primario.TButton",
            command=self.iniciar_organizacao,
        )
        self.btn_iniciar.grid(row=0, column=0, padx=(0, 10), sticky="w")

        # Botão Desfazer (perigo - inicialmente desabilitado)
        self.btn_desfazer = ttk.Button(
            btn_frame,
            text="↩ Desfazer Organização",
            style="Perigo.TButton",
            command=self.desfazer_organizacao,
            state=tk.DISABLED,
        )
        self.btn_desfazer.grid(row=0, column=2, padx=(0, 10), sticky="w")

        # Botão Limpar histórico (secundário)
        self.btn_limpar_hist = ttk.Button(
            btn_frame,
            text="🗑️ Limpar Histórico",
            style="Secundario.TButton",
            command=self.limpar_historico,
        )
        self.btn_limpar_hist.grid(row=0, column=3, sticky="e")

        # Verifica histórico existente
        self.verificar_historico_existente()

    def _configurar_atalhos(self) -> None:
        """Configura atalhos de teclado."""
        self.root.bind("<F5>", lambda e: self.atualizar_preview())
        self.root.bind(
            "<Control-Return>",
            lambda e: self.iniciar_organizacao() if self.btn_iniciar["state"] == "normal" else None,
        )
        self.root.bind(
            "<Control-z>",
            lambda e: (
                self.desfazer_organizacao() if self.btn_desfazer["state"] == "normal" else None
            ),
        )
        self.root.bind("<Escape>", lambda e: self._cancelar_operacao())

    # ==================== CALLBACKS UI ====================

    def _ao_alterar_pasta(self, event=None) -> None:
        """Debounce para atualizar preview ao digitar pasta."""
        if self._preview_debounce_id:
            self.root.after_cancel(self._preview_debounce_id)
        self._preview_debounce_id = self.root.after(500, self.atualizar_preview)

    def _ao_alterar_opcoes(self) -> None:
        """Callback ao alterar checkbox renomear."""
        self.atualizar_preview()

    def _ao_duplo_clique(self, event) -> None:
        """Abre local do arquivo no explorador."""
        item = self.tree_preview.selection()
        if item:
            valores = self.tree_preview.item(item[0], "values")
            if valores:
                arquivo_original = valores[0]
                pasta = Path(self.pasta_selecionada.get())
                arquivo_path = pasta / arquivo_original
                if arquivo_path.exists():
                    import subprocess

                    if sys.platform == "win32":
                        subprocess.run(["explorer", "/select,", str(arquivo_path)])
                    elif sys.platform == "darwin":
                        subprocess.run(["open", "-R", str(arquivo_path)])
                    else:
                        subprocess.run(["xdg-open", str(pasta)])

    def _ao_tecla_tree(self, event) -> None:
        """Atalhos no treeview."""
        if event.keysym == "Delete":
            self._remover_da_preview()
        elif event.keysym == "Return":
            self._ao_duplo_clique(event)

    def _ordenar_coluna(self, coluna: str) -> None:
        """Ordena treeview por coluna."""
        # Implementação simples - alterna ascendente/descendente
        pass

    def _expandir_tudo(self) -> None:
        """Expande todos os itens (para futuro uso com agrupamento)."""
        pass

    def _colapsar_tudo(self) -> None:
        """Colapsa todos os itens."""
        pass

    def _copiar_lista(self) -> None:
        """Copiar lista de movimentos para clipboard."""
        if not self.movimentos_preview:
            return

        linhas = []
        for m in self.movimentos_preview:
            linhas.append(f"{m['arquivo']} -> {m['categoria']}/{m['novo_nome']}")

        texto = "\n".join(linhas)
        self.root.clipboard_clear()
        self.root.clipboard_append(texto)
        self.lbl_status.config(text=f"📋 {len(linhas)} itens copiados para a área de transferência")

    def _remover_da_preview(self) -> None:
        """Remove itens selecionados da preview (apenas visual)."""
        # Apenas remove da visualização, não do disco
        for item in self.tree_preview.selection():
            self.tree_preview.delete(item)

    def _cancelar_operacao(self) -> None:
        """Cancela operação em andamento."""
        if self.organizando:
            if messagebox.askyesno("Cancelar", "Deseja cancelar a operação em andamento?"):
                self.organizando = False
                self.btn_iniciar.config(state=tk.NORMAL, text="🚀 Iniciar Organização")
                self.btn_desfazer.config(state=tk.NORMAL if self.historico_atual else tk.DISABLED)
                self.lbl_status.config(
                    text="⚠️ Operação cancelada pelo usuário", style="Aviso.TLabel"
                )

    def _ao_fechar(self) -> None:
        """Handler para fechamento da janela."""
        if self.organizando:
            if not messagebox.askokcancel(
                "Sair", "Uma operação está em andamento. Deseja realmente sair?"
            ):
                return
        self.root.destroy()

    # ==================== TOOLTIP HELPER ====================

    def _criar_tooltip(self, widget: tk.Widget, texto: str) -> None:
        """Cria tooltip simples para widget."""

        def mostrar(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = ttk.Label(
                tooltip, text=texto, background="#ffffe0", relief="solid", borderwidth=1, padding=5
            )
            label.pack()
            widget.tooltip = tooltip

        def esconder(event):
            if hasattr(widget, "tooltip"):
                widget.tooltip.destroy()
                del widget.tooltip

        widget.bind("<Enter>", mostrar)
        widget.bind("<Leave>", esconder)

    # ==================== LÓGICA DE NEGÓCIO ====================

    def selecionar_pasta(self) -> None:
        """Abre diálogo para selecionar pasta."""
        pasta = filedialog.askdirectory(
            initialdir=self.pasta_selecionada.get(),
            title="Selecione a pasta para organizar",
            mustexist=True,
        )
        if pasta:
            self.pasta_selecionada.set(pasta)
            self.atualizar_preview()

    def atualizar_preview(self) -> None:
        """Atualiza a prévia baseada na pasta selecionada."""
        # Limpa tree
        for item in self.tree_preview.get_children():
            self.tree_preview.delete(item)

        pasta = Path(self.pasta_selecionada.get())
        renomear = self.renomear_var.get()

        # Valida pasta
        if not pasta.exists() or not pasta.is_dir():
            self.lbl_estatisticas.config(
                text="❌ Pasta inválida ou não encontrada", style="Erro.TLabel"
            )
            self.btn_iniciar.config(state=tk.DISABLED)
            return

        # Escaneia
        try:
            self.movimentos_preview = escanear_pasta(pasta, renomear)
        except Exception as e:
            logger.error(f"Erro ao escanear pasta: {e}")
            self.lbl_estatisticas.config(text=f"❌ Erro ao ler pasta: {e}", style="Erro.TLabel")
            self.btn_iniciar.config(state=tk.DISABLED)
            return

        if not self.movimentos_preview:
            self.lbl_estatisticas.config(
                text="📭 Nenhum arquivo para organizar", style="Aviso.TLabel"
            )
            self.btn_iniciar.config(state=tk.DISABLED)
            return

        # Conta por categoria
        contagem: Dict[str, int] = {}
        for mov in self.movimentos_preview:
            cat = mov["categoria"]
            contagem[cat] = contagem.get(cat, 0) + 1

        stats_text = f"📊 {len(self.movimentos_preview)} arquivo(s) | " + " | ".join(
            [f"{k}: {v}" for k, v in sorted(contagem.items())]
        )
        self.lbl_estatisticas.config(text=stats_text, style="Estatisticas.TLabel")
        self.btn_iniciar.config(state=tk.NORMAL)

        # Preenche tree
        for mov in self.movimentos_preview:
            tag = mov["categoria_enum"].name.lower()
            tamanho_str = self._formatar_tamanho(mov.get("tamanho", 0))
            self.tree_preview.insert(
                "",
                tk.END,
                values=(mov["arquivo"], mov["categoria"], mov["novo_nome"], tamanho_str),
                tags=(tag,),
            )

    def _formatar_tamanho(self, bytes_: float) -> str:
        """Formata tamanho para exibição."""
        for unidade in ["B", "KB", "MB", "GB"]:
            if bytes_ < 1024.0:
                return f"{bytes_:.1f} {unidade}"
            bytes_ /= 1024.0
        return f"{bytes_:.1f} TB"

    def verificar_historico_existente(self) -> None:
        """Verifica se há histórico salvo para a pasta atual."""
        historico = carregar_historico()
        if (
            historico
            and historico.pasta_base == self.pasta_selecionada.get()
            and historico.movimentos
        ):
            self.historico_atual = historico
            self.btn_desfazer.config(state=tk.NORMAL)
            self.lbl_status.config(
                text=f"⚠️ Histórico anterior ({len(historico.movimentos)} arquivos) - Clique em Desfazer para restaurar",
                style="Aviso.TLabel",
            )

    def iniciar_organizacao(self) -> None:
        """Inicia a organização em thread separada."""
        if self.organizando:
            return

        pasta = Path(self.pasta_selecionada.get())
        if not pasta.exists() or not pasta.is_dir():
            messagebox.showerror("Erro", "Pasta inválida!")
            return

        renomear = self.renomear_var.get()

        # Confirmação
        total = len(self.movimentos_preview)
        msg = (
            f"Organizar {total} arquivo(s) em:\n{pasta}\n\n"
            f"Renomear com data: {'Sim' if renomear else 'Não'}\n\n"
            f"As pastas de categoria serão criadas automaticamente."
        )
        if not messagebox.askyesno("Confirmar Organização", msg):
            return

        self.organizando = True
        self.btn_iniciar.config(state=tk.DISABLED, text="⏳ Organizando...")
        self.btn_desfazer.config(state=tk.DISABLED)
        self.btn_limpar_hist.config(state=tk.DISABLED)
        self.chk_renomear.config(state=tk.DISABLED)
        self.entry_pasta.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.lbl_status.config(text="Iniciando...", style="Status.TLabel")

        thread = Thread(
            target=self._executar_organizacao_thread, args=(pasta, renomear), daemon=True
        )
        thread.start()

    def _executar_organizacao_thread(self, pasta: Path, renomear: bool) -> None:
        """Thread worker para organização."""

        def callback_prog(
            atual: int, total: int, arquivo: str, categoria: str, novo_nome: str
        ) -> None:
            self.root.after(
                0, lambda: self._atualizar_progresso(atual, total, arquivo, categoria, novo_nome)
            )

        try:
            historico = executar_organizacao(pasta, renomear, callback_prog)
            self.root.after(0, lambda: self._finalizar_organizacao(historico))
        except PastaInvalidaError as exc:
            self._agendar_erro(str(exc))
        except PermissaoError as exc:
            self._agendar_erro(
                f"{exc}\n\nFeche programas usando os arquivos ou execute como Administrador."
            )
        except OrganizadorError as exc:
            self._agendar_erro(str(exc))
        except Exception as exc:
            logger.exception("Erro inesperado na organização")
            self._agendar_erro(f"Erro inesperado: {exc}")

    def _atualizar_progresso(
        self, atual: int, total: int, arquivo: str, categoria: str, novo_nome: str
    ) -> None:
        """Atualiza UI com progresso."""
        pct = (atual / total) * 100 if total > 0 else 0
        self.progress_var.set(pct)
        self.lbl_status.config(text=f"📦 [{atual}/{total}] {arquivo} → {categoria}/{novo_nome}")

    def _finalizar_organizacao(self, historico: HistoricoOrganizacao) -> None:
        """Finaliza organização com sucesso."""
        self.organizando = False
        self.historico_atual = historico

        # Salva histórico (nova API segura)
        try:
            salvar_historico(historico)
        except Exception as e:
            logger.warning(f"Não foi possível salvar histórico: {e}")

        self.progress_var.set(100)
        self.lbl_status.config(
            text=f"✅ Concluído! {len(historico.movimentos)} arquivo(s) organizado(s)",
            style="Estatisticas.TLabel",
        )
        self.btn_iniciar.config(state=tk.NORMAL, text="🚀 Iniciar Organização")
        self.btn_desfazer.config(state=tk.NORMAL)
        self.btn_limpar_hist.config(state=tk.NORMAL)
        self.chk_renomear.config(state=tk.NORMAL)
        self.entry_pasta.config(state=tk.NORMAL)

        # Atualiza preview
        self.atualizar_preview()

        # Dialog de sucesso
        messagebox.showinfo(
            "Sucesso!",
            f"Organização concluída!\n\n"
            f"{len(historico.movimentos)} arquivo(s) movido(s) para pastas categorizadas.\n\n"
            f"Use o botão 'Desfazer' se quiser restaurar.",
        )

    def _agendar_erro(self, mensagem: str) -> None:
        """Agenda exibição de erro na thread principal."""
        self.root.after(0, partial(self._erro_organizacao, mensagem))

    def _agendar_erro_desfazer(self, mensagem: str) -> None:
        """Agenda finalização de desfazer com erro na thread principal."""
        self.root.after(0, partial(self._finalizar_desfazer, 0, [mensagem]))

    def _erro_organizacao(self, mensagem: str) -> None:
        """Trata erro durante organização."""
        self.organizando = False
        self.progress_var.set(0)
        self.lbl_status.config(text=f"❌ Erro: {mensagem}", style="Erro.TLabel")
        self.btn_iniciar.config(state=tk.NORMAL, text="🚀 Iniciar Organização")
        self.btn_limpar_hist.config(state=tk.NORMAL)
        self.chk_renomear.config(state=tk.NORMAL)
        self.entry_pasta.config(state=tk.NORMAL)
        self.verificar_historico_existente()
        messagebox.showerror("Erro na Organização", mensagem)

    def desfazer_organizacao(self) -> None:
        """Desfaz a última organização."""
        if not self.historico_atual or not self.historico_atual.movimentos:
            messagebox.showwarning("Aviso", "Nenhum histórico para desfazer!")
            return

        total = len(self.historico_atual.movimentos)
        msg = (
            f"Desfazer a organização de {total} arquivo(s)?\n\n"
            f"Os arquivos voltarão para a pasta original:\n{self.historico_atual.pasta_base}\n\n"
            f"Pastas de categoria vazias serão removidas."
        )
        if not messagebox.askyesno("Confirmar Desfazer", msg, icon="warning"):
            return

        self.organizando = True
        self.btn_desfazer.config(state=tk.DISABLED, text="⏳ Desfazendo...")
        self.btn_iniciar.config(state=tk.DISABLED)
        self.btn_limpar_hist.config(state=tk.DISABLED)
        self.progress_var.set(0)

        thread = Thread(target=self._desfazer_thread, daemon=True)
        thread.start()

    def _desfazer_thread(self) -> None:
        """Thread worker para desfazer."""

        def callback_prog(atual: int, total: int, arquivo: str, acao: str, novo_nome: str) -> None:
            self.root.after(
                0,
                lambda: self._atualizar_progresso_desfazer(atual, total, arquivo, acao, novo_nome),
            )

        historico = self.historico_atual
        if historico is None:
            self.root.after(
                0, lambda: self._finalizar_desfazer(0, ["Nenhum histórico para desfazer"])
            )
            return

        try:
            sucessos, erros = desfazer_organizacao(historico, callback_prog)
            self.root.after(0, lambda: self._finalizar_desfazer(sucessos, erros))
        except Exception as exc:
            logger.exception("Erro ao desfazer")
            self._agendar_erro_desfazer(str(exc))

    def _atualizar_progresso_desfazer(
        self, atual: int, total: int, arquivo: str, acao: str, novo_nome: str
    ) -> None:
        """Atualiza UI durante desfazer."""
        pct = (atual / total) * 100 if total > 0 else 0
        self.progress_var.set(pct)
        self.lbl_status.config(text=f"{acao} [{atual}/{total}] {arquivo} → {novo_nome}")

    def _finalizar_desfazer(self, sucessos: int, erros: List[str]) -> None:
        """Finaliza desfazer."""
        self.organizando = False

        if erros:
            msg = (
                f"Desfeito parcialmente: {sucessos} arquivo(s) restaurado(s), {len(erros)} erro(s)."
            )
            self.lbl_status.config(text=msg, style="Aviso.TLabel")
            messagebox.showwarning("Desfazer Parcial", msg + "\n\nErros:\n" + "\n".join(erros[:10]))
        else:
            msg = f"✅ Desfeito com sucesso! {sucessos} arquivo(s) restaurado(s)."
            self.lbl_status.config(text=msg, style="Estatisticas.TLabel")
            messagebox.showinfo("Sucesso", msg)

            # Limpa histórico
            self.historico_atual = None
            if self.arquivo_historico.exists():
                try:
                    self.arquivo_historico.unlink()
                except Exception:
                    pass

        self.progress_var.set(100)
        self.btn_desfazer.config(state=tk.DISABLED, text="↩ Desfazer Organização")
        self.btn_iniciar.config(state=tk.NORMAL)
        self.btn_limpar_hist.config(state=tk.NORMAL)
        self.atualizar_preview()

    def limpar_historico(self) -> None:
        """Limpa o histórico salvo."""
        if not self.arquivo_historico.exists():
            messagebox.showinfo("Limpo", "Nenhum histórico para limpar.")
            return

        if messagebox.askyesno(
            "Confirmar",
            "Remover histórico de desfazer?\nNão será mais possível desfazer a última organização.",
        ):
            try:
                self.arquivo_historico.unlink()
                self.historico_atual = None
                self.btn_desfazer.config(state=tk.DISABLED)
                self.lbl_status.config(text="🗑️ Histórico limpo", style="Status.TLabel")
                messagebox.showinfo("Limpo", "Histórico de desfazer removido.")
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao limpar histórico: {e}")


def main_gui() -> int:
    """Ponto de entrada da GUI."""
    # Configura logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    # Configura DPI awareness no Windows
    if sys.platform == "win32":
        try:
            from ctypes import windll

            windll.shcore.SetProcessDpiAwareness(1)
        except Exception:
            pass

    root = tk.Tk()
    OrganizadorGUI(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    sys.exit(main_gui())
