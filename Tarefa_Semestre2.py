import customtkinter as ctk
import mysql.connector
from datetime import datetime
from tkinter import messagebox
import tkinter as tk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#CONFIGURAÇÃO DO BANCO

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '1234',
    'database': 'gestao_tarefas'
}

PRIORIDADE = {1: "Baixa", 2: "Média", 3: "Alta", 4: "Urgente"}
PRIORIDADE_INV = {"Baixa": 1, "Média": 2, "Alta": 3, "Urgente": 4}
PRIORIDADE_COR = {1: "#4CAF50", 2: "#2196F3", 3: "#FF9800", 4: "#F44336"}

#RETORNA UMA CONEXAO DO BANCO USANDO DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG)

#CONECTA E CRIA BANCO DE DADOS E A TABELA DE TAREFAS, SE NAO EXISTIREM

def inicializar_banco():
    conn = mysql.connector.connect(
        host=DB_CONFIG['host'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password']
    )
    cur = conn.cursor()
    cur.execute("CREATE DATABASE IF NOT EXISTS gestao_tarefas CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")

    conn.close()

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id         INT AUTO_INCREMENT PRIMARY KEY,
            titulo     VARCHAR(255) NOT NULL,
            descricao  TEXT,
            disciplina VARCHAR(100),
            prioridade TINYINT NOT NULL,
            data       DATETIME NOT NULL,
            ok         BOOLEAN NOT NULL DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()

#RETORNA QUANTOS DIAS FALTAM ATÉ A DATA (OU ATRASO OU EM NEGATIVO)

def dias_restantes(data):
    return (data - datetime.now()).days

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Gestão de Tarefas Acadêmicas")
        self.geometry("1100x680")
        self.minsize(900, 600)
        self.configure(fg_color="#0f0f13")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.show_frame("dashboard")

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#17171f")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)

        logo = ctk.CTkLabel(self.sidebar, text="📚 Tarefas", font=ctk.CTkFont("Georgia", 22, "bold"),
                            text_color="#e8d5b0")
        logo.grid(row=0, column=0, padx=24, pady=(32, 8), sticky="w")

        sub = ctk.CTkLabel(self.sidebar, text="Acadêmicas", font=ctk.CTkFont(size=11),
                           text_color="#666680")
        sub.grid(row=1, column=0, padx=24, pady=(0, 28), sticky="w")

        sep = ctk.CTkFrame(self.sidebar, height=1, fg_color="#2a2a3a")
        sep.grid(row=2, column=0, padx=16, pady=(0, 20), sticky="ew")

        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "  ⬡  Dashboard",   "#dashboard"),
            ("cadastrar",  "  ＋  Nova Tarefa",  "#cadastrar"),
            ("listar",     "  ≡  Todas as Tarefas", "#listar"),
            ("relatorios", "  ◈  Relatórios",   "#relatorios"),
        ]
        for i, (key, label, _) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self.sidebar, text=label, anchor="w",
                font=ctk.CTkFont(size=13),
                fg_color="transparent", hover_color="#23233a",
                text_color="#a0a0c0", corner_radius=8, height=42,
                command=lambda k=key: self.show_frame(k)
            )
            btn.grid(row=i+3, column=0, padx=12, pady=3, sticky="ew")
            self.nav_buttons[key] = btn

        self.sidebar.grid_columnconfigure(0, weight=1)

        ver = ctk.CTkLabel(self.sidebar, text="v1.0  •  MySQL 8.0",
                           font=ctk.CTkFont(size=10), text_color="#444458")
        ver.grid(row=11, column=0, padx=24, pady=20, sticky="sw")

    def _build_main(self):
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color="#0f0f13")
        self.main.grid(row=0, column=1, sticky="nsew", padx=0)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(0, weight=1)

        self.frames = {}
        for F in (DashboardFrame, CadastrarFrame, ListarFrame, RelatoriosFrame):
            frame = F(self.main, self)
            self.frames[F.name] = frame
            frame.grid(row=0, column=0, sticky="nsew", padx=32, pady=24)

#ATUALIZA O DESTAQUE DOS BOTÕES
  def show_frame(self, name):
        for key, btn in self.nav_buttons.items():
            if key == name:
                btn.configure(fg_color="#23233a", text_color="#e8d5b0")
            else:
                btn.configure(fg_color="transparent", text_color="#a0a0c0")

# ESCONDE TODOS OS FRAMES
        for frame in self.frames.values():
            frame.grid_remove()

        frame = self.frames[name]
        frame.grid()
        if hasattr(frame, "refresh"):
            frame.refresh()


class DashboardFrame(ctk.CTkFrame):
    name = "dashboard"

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)

        ctk.CTkLabel(self, text="Dashboard", font=ctk.CTkFont("Georgia", 28, "bold"),
                     text_color="#e8d5b0").grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 6))
        self.subtitle = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=12), text_color="#555570")
        self.subtitle.grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 24))

#CARDS PRINCIPAIS
        self.cards = []
        configs = [
            ("Total", "#2a2a3a", "#e8d5b0"),
            ("Concluídas", "#1a2e1a", "#4CAF50"),
            ("Pendentes", "#1e1e2e", "#2196F3"),
            ("Atrasadas", "#2e1a1a", "#F44336"),
        ]
        for i, (label, bg, color) in enumerate(configs):
            card = ctk.CTkFrame(self, fg_color=bg, corner_radius=12, height=100)
            card.grid(row=2, column=i, padx=(0 if i == 0 else 10, 0), sticky="ew")
            card.grid_columnconfigure(0, weight=1)
            lbl = ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11), text_color="#888899")
            lbl.grid(row=0, column=0, padx=20, pady=(18, 2), sticky="w")
            num = ctk.CTkLabel(card, text="—", font=ctk.CTkFont("Georgia", 34, "bold"), text_color=color)
            num.grid(row=1, column=0, padx=20, pady=(0, 16), sticky="w")
            self.cards.append(num)

        sep = ctk.CTkFrame(self, height=1, fg_color="#1e1e2e")
        sep.grid(row=3, column=0, columnspan=4, sticky="ew", pady=24)

        ctk.CTkLabel(
            self,
            text="Próximas Entregas (7 dias)",
            font=ctk.CTkFont(size=14,
            weight="bold"),
            text_color="#c0c0d8"
        ).grid(row=4, column=0, columnspan=4, sticky="w", pady=(0, 12))

#LISTA PROXIMAS ENTREGAS
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#13131b", corner_radius=12, height=240)
        self.scroll.grid(row=5, column=0, columnspan=4, sticky="ew")
        self.scroll.grid_columnconfigure(0, weight=1)

    def refresh(self):
        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.subtitle.configure(text=f"Atualizado em {now}")
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM tarefas")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE ok=TRUE")
            conc = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE ok=FALSE")
            pend = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE data < NOW() AND ok=FALSE")
            atr = cur.fetchone()[0]
            conn.close()

#LIMPA LISTA DE PRÓXIMAS
            for widget in self.scroll.winfo_children():
                widget.destroy()

            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM tarefas WHERE data >= NOW() AND data <= DATE_ADD(NOW(), INTERVAL 7 DAY) AND ok=FALSE ORDER BY data")
            prox = cur.fetchall()
            conn.close()

            self.cards[0].configure(text=str(total))
            self.cards[1].configure(text=str(conc))
            self.cards[2].configure(text=str(pend))
            self.cards[3].configure(text=str(atr))

            if not prox:
                ctk.CTkLabel(self.scroll, text="Nenhuma entrega nos próximos 7 dias 🎉",
                             text_color="#555570", font=ctk.CTkFont(size=13)).grid(padx=20, pady=20)
            else:
                for t in prox:
                    self._row(t)
        except Exception as e:
            ctk.CTkLabel(self.scroll, text=f"Erro: {e}", text_color="#F44336").grid(padx=20, pady=10)

    def _row(self, t):
        row = ctk.CTkFrame(self.scroll, fg_color="#1a1a25", corner_radius=8)
        row.grid(sticky="ew", padx=8, pady=4)
        row.grid_columnconfigure(1, weight=1)
        dias = dias_restantes(t['data'])
        cor = PRIORIDADE_COR[t['prioridade']]
        dot = ctk.CTkLabel(row, text="●", text_color=cor, font=ctk.CTkFont(size=14))
        dot.grid(row=0, column=0, padx=(14, 8), pady=12)
        ctk.CTkLabel(row,
                     text=t['titulo'],
                     font=ctk.CTkFont(size=13, weight="bold"),
                     text_color="#d0d0e8",
                     anchor="w"
                    ).grid(row=0, column=1, sticky="w")

        ctk.CTkLabel(row,
                     text=f"{t['disciplina']}  •  {dias}d", font=ctk.CTkFont(size=11),
                     text_color="#666680", anchor="e"
                    ).grid(row=0, column=2, padx=16)


class CadastrarFrame(ctk.CTkFrame):
    name = "cadastrar"

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(self, text="Nova Tarefa", font=ctk.CTkFont("Georgia", 28, "bold"),
                     text_color="#e8d5b0").grid(row=0, column=0, sticky="w", pady=(0, 24))

        card = ctk.CTkFrame(self, fg_color="#17171f", corner_radius=16)
        card.grid(row=1, column=0, sticky="ew")
        card.grid_columnconfigure((0, 1), weight=1)

        def field(label, row, col=0, colspan=1, widget=None):
            ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=12),
                         text_color="#666680").grid(row=row*2, column=col, columnspan=colspan,
                                                    sticky="w", padx=20, pady=(16, 2))
            if widget is None:
                e = ctk.CTkEntry(card, height=38, fg_color="#0f0f13", border_color="#2a2a3a",
                                 text_color="#d0d0e8", corner_radius=8)
            else:
                e = widget
            e.grid(row=row*2+1, column=col, columnspan=colspan, sticky="ew", padx=20, pady=(0, 4))
            return e

        self.titulo = field("Título da Tarefa", 0, 0, 2)
        self.desc = field("Descrição", 1, 0, 2)
        self.disc = field("Disciplina", 2, 0)
        self.data = field("Data de Entrega (DD/MM/AAAA)", 2, 1)

        ctk.CTkLabel(card, text="Prioridade", font=ctk.CTkFont(size=12),
                     text_color="#666680").grid(row=6, column=0, sticky="w", padx=20, pady=(16, 2))
        self.prio = ctk.CTkOptionMenu(card, values=["Baixa", "Média", "Alta", "Urgente"],
                                      fg_color="#0f0f13", button_color="#23233a",
                                      button_hover_color="#2e2e48", text_color="#d0d0e8",
                                      dropdown_fg_color="#1a1a25", corner_radius=8, height=38)
        self.prio.grid(row=7, column=0, sticky="ew", padx=20, pady=(0, 20))

        btn = ctk.CTkButton(card, text="  Cadastrar Tarefa  ", height=44,
                            fg_color="#3a3a6a", hover_color="#4a4a8a",
                            text_color="#e8d5b0", font=ctk.CTkFont(size=14, weight="bold"),
                            corner_radius=10, command=self.cadastrar)
        btn.grid(row=7, column=1, padx=20, pady=(0, 20), sticky="ew")

    def cadastrar(self):
        titulo = self.titulo.get().strip()
        desc = self.desc.get().strip()
        disc = self.disc.get().strip()
        data_str = self.data.get().strip()
        prio_str = self.prio.get()

        if not titulo:
            messagebox.showerror("Erro", "O título é obrigatório!")
            return
        try:
            dt = datetime.strptime(data_str, "%d/%m/%Y")
        except:
            messagebox.showerror("Erro", "Data inválida! Use DD/MM/AAAA")
            return
        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tarefas (titulo, descricao, disciplina, prioridade, data, ok) VALUES (%s,%s,%s,%s,%s,%s)",
                (titulo, desc, disc, PRIORIDADE_INV[prio_str], dt, False)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", f"Tarefa '{titulo}' cadastrada!")

#LIMPA OS CAMPOS DE ENTRADA APÓS CADASTRO
            for w in [self.titulo, self.desc, self.disc, self.data]:
                w.delete(0, "end")
            self.prio.set("Baixa")
        except Exception as e:
            messagebox.showerror("Erro", str(e))


class ListarFrame(ctk.CTkFrame):
    name = "listar"

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

#CABEÇALHO COM TITULO E BOTÕES
        hdr = ctk.CTkFrame(self, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        hdr.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            hdr,
            text="Todas as Tarefas",
            font=ctk.CTkFont("Georgia", 28, "bold"),
            text_color="#e8d5b0"
            ).grid(row=0, column=0, sticky="w")

        btns = ctk.CTkFrame(hdr, fg_color="transparent")
        btns.grid(row=0, column=1, sticky="e")

        ctk.CTkButton(btns,
                      text="↻ Atualizar",
                      height=36,
                      width=110,
                      fg_color="#1e1e2e",
                      hover_color="#23233a",
                      text_color="#a0a0c0",
                      corner_radius=8,
                      command=self.refresh
                      ).grid(row=0, column=0, padx=(0, 8))

        ctk.CTkButton(btns,
                      text="＋ Nova",
                      height=36,
                      width=90,
                      fg_color="#3a3a6a",
                      hover_color="#4a4a8a",
                      text_color="#e8d5b0",
                      corner_radius=8,
                      command=lambda: app.show_frame("cadastrar")#VAI PARA TELA DE CADASTRO
                      ).grid(row=0, column=1)

#FILTRO DE VISUALIZAÇÕES (TODAS, PENDENTES, CONCLUIDAS)
        self.filtro = ctk.CTkSegmentedButton(
            self, values=["Todas", "Pendentes", "Concluídas"],
            fg_color="#17171f",
            selected_color="#3a3a6a",
            selected_hover_color="#4a4a8a",
            unselected_color="#17171f",
            text_color="#a0a0c0",                                           command=self.refresh
            )
        self.filtro.set("Todas")
        self.filtro.grid(row=1, column=0, sticky="w", pady=(0, 16))

#LISTA ROLAVEL DE TAREFAS
        self.scroll = ctk.CTkScrollableFrame(self, fg_color="#13131b", corner_radius=12)
        self.scroll.grid(row=2, column=0, sticky="nsew")
        self.scroll.grid_columnconfigure(0, weight=1)

#RECARREGA A LISTA DE TAREFAS DE ACORDO COM O FILTRO
    def refresh(self, *_):
        for w in self.scroll.winfo_children():
            w.destroy()

        filtro = self.filtro.get()

        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)

            if filtro == "Pendentes":
                cur.execute("SELECT * FROM tarefas WHERE ok=FALSE ORDER BY prioridade DESC, data")
            elif filtro == "Concluídas":
                cur.execute("SELECT * FROM tarefas WHERE ok=TRUE ORDER BY data DESC")
            else:
                cur.execute("SELECT * FROM tarefas ORDER BY ok, prioridade DESC, data")

            tarefas = cur.fetchall()
            conn.close()

            if not tarefas:
                ctk.CTkLabel(
                    self.scroll,
                    text="Nenhuma tarefa encontrada.",                             text_color="#555570", font=ctk.CTkFont(size=13)
                    ).grid(padx=20, pady=30)
            else:
                for t in tarefas:
                    self._row(t)
        except Exception as e:
            ctk.CTkLabel(
                self.scroll,
                text=f"Erro: {e}",
                text_color="#F44336"
                ).grid(padx=20, pady=10)

#CRIA UMA LINHA VISUAL PARA UMA TAREFA NA LISTA
    def _row(self, t):
        cor = PRIORIDADE_COR[t['prioridade']]
        bg = "#1d1d2a" if not t['ok'] else "#151520"

        row = ctk.CTkFrame(self.scroll, fg_color=bg, corner_radius=10)
        row.grid(sticky="ew", padx=8, pady=4)
        row.grid_columnconfigure(1, weight=1)

#PONTO DE PRIORIDADE
        dot = ctk.CTkLabel(
            row,
            text="●",
            text_color=cor if not t['ok'] else "#444458",                           font=ctk.CTkFont(size=16)
            )
        dot.grid(row=0, column=0, rowspan=2, padx=(16, 10), pady=14)

        titulo_text = t['titulo'] if not t['ok'] else f"✓ {t['titulo']}"
        titulo_color = "#d0d0e8" if not t['ok'] else "#555570"

        ctk.CTkLabel(
            row,
            text=titulo_text,
            font=ctk.CTkFont(size=13, weight="bold"),                     text_color=titulo_color, anchor="w"
            ).grid(row=0, column=1, sticky="w", pady=(12, 2))

#INFORMAÇOES MENORES (DISCIPLINA, PRIORIDADE, DATA)
        info = f"{t['disciplina'] or '—'}  •  {PRIORIDADE[t['prioridade']]}  •  {t['data'].strftime('%d/%m/%Y')}"
        ctk.CTkLabel(
            row,
            text=info,
            font=ctk.CTkFont(size=11),
            text_color="#555570", anchor="w"
        ).grid(row=1, column=1, sticky="w", pady=(0, 12))

#DIAS RESTANTES OU DE ATRASO
        dias = dias_restantes(t['data'])
        if not t['ok']:
            dias_txt = f"{dias}d" if dias >= 0 else f"Atrasada {abs(dias)}d"
            dias_cor = "#4CAF50" if dias > 3 else ("#FF9800" if dias >= 0 else "#F44336")

            ctk.CTkLabel(
                row,
                text=dias_txt,
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=dias_cor
            ).grid(row=0, column=2, rowspan=2, padx=12)

#BARRA DE AÇAO (CONCLUIR / EXCLUIR)
        actions = ctk.CTkFrame(row, fg_color="transparent")
        actions.grid(row=0, column=3, rowspan=2, padx=(0, 12))

        if not t['ok']:
            ctk.CTkButton(
                actions,
                text="✓",
                width=32,
                height=32,
                fg_color="#1a2e1a",
                hover_color="#1f3d1f",
                text_color="#4CAF50",
                corner_radius=8,
                command=lambda tid=t['id']: self.concluir(tid)
            ).grid(row=0, column=0, padx=2)

        ctk.CTkButton(actions,
                      text="✕",
                      width=32,
                      height=32,
                      fg_color="#2e1a1a",
                      hover_color="#3d1f1f",
                      text_color="#F44336",
                      corner_radius=8,
                      command=lambda tid=t['id'], ttl=t['titulo']: self.excluir(tid, ttl)
                    ).grid(row=0, column=1, padx=2)

#MARCA COMO TAREFA CONFLUIDA
    def concluir(self, tid):
        if messagebox.askyesno("Confirmar", "Marcar como concluída?"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE tarefas SET ok=TRUE WHERE id=%s", (tid,))
            conn.commit()
            conn.close()
            self.refresh()

#EXCLUI TAREFA APÓS CONFIRMAÇAO
    def excluir(self, tid, titulo):
        if messagebox.askyesno("Confirmar", f"Excluir '{titulo}'?"):
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM tarefas WHERE id=%s", (tid,))
            conn.commit()
            conn.close()
            self.refresh()


class RelatoriosFrame(ctk.CTkFrame):
    name = "relatorios"

    def __init__(self, parent, app):
        super().__init__(parent, fg_color="transparent")
        self.app = app
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(self,
                     text="Relatórios",
                     font=ctk.CTkFont("Georgia", 28, "bold"),
                     text_color="#e8d5b0"
                    ).grid(row=0, column=0, sticky="w", pady=(0, 20))

        tabs = ctk.CTkTabview(self, fg_color="#17171f", segmented_button_fg_color="#0f0f13",
                              segmented_button_selected_color="#3a3a6a",
                              segmented_button_selected_hover_color="#4a4a8a",
                              text_color="#a0a0c0", corner_radius=12
                            )

        tabs.grid(row=1, column=0, sticky="nsew")
        tabs.add("Atrasadas")
        tabs.add("Por Prioridade")
        tabs.add("Estatísticas")

        self.tab_atr = tabs.tab("Atrasadas")
        self.tab_prio = tabs.tab("Por Prioridade")
        self.tab_stats = tabs.tab("Estatísticas")

        for tab in [self.tab_atr, self.tab_prio, self.tab_stats]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

#SCROLL PARA TAREFAS ATRASADAS
        self.scroll_atr = ctk.CTkScrollableFrame(self.tab_atr, fg_color="transparent")
        self.scroll_atr.grid(row=0, column=0, sticky="nsew")
        self.scroll_atr.grid_columnconfigure(0, weight=1)

#SCROLL PARA TAREFAS POR PRIORIDADE
        self.scroll_prio = ctk.CTkScrollableFrame(self.tab_prio, fg_color="transparent")
        self.scroll_prio.grid(row=0, column=0, sticky="nsew")
        self.scroll_prio.grid_columnconfigure(0, weight=1)

#ESTASTÍSTICAS EM FORMA DE CARD
        self.stats_frame = ctk.CTkFrame(self.tab_stats, fg_color="transparent")
        self.stats_frame.grid(row=0, column=0, sticky="nsew")
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)

#ATUALIZA TODOS OS RELATORIOS
    def refresh(self):
        self._load_atrasadas()
        self._load_prioridade()
        self._load_stats()

#CARREGA TAREFAS ATRASADAS
    def _load_atrasadas(self):
        for w in self.scroll_atr.winfo_children():
            w.destroy()

        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT * FROM tarefas WHERE data < NOW() AND ok=FALSE ORDER BY data")
            atr = cur.fetchall()
            conn.close()
            if not atr:
                ctk.CTkLabel(self.scroll_atr,
                             text="Nenhuma tarefa atrasada 🎉",
                             text_color="#4CAF50",
                             font=ctk.CTkFont(size=14)
                            ).grid(pady=30)
            else:
                for t in atr:
                    row = ctk.CTkFrame(self.scroll_atr, fg_color="#2e1a1a", corner_radius=8)
                    row.grid(sticky="ew", padx=4, pady=4)
                    row.grid_columnconfigure(0, weight=1)

                    ctk.CTkLabel(
                        row,
                        text=t['titulo'],
                        font=ctk.CTkFont(size=13, weight="bold"),                                 text_color="#F44336",
                        anchor="w"
                    ).grid(row=0, column=0, sticky="w", padx=16, pady=(10, 2))


                    ctk.CTkLabel(
                        row,
                        text=f"{t['disciplina'] or '—'}  •  Atrasada há {abs(dias_restantes(t['data']))} dias",
                        font=ctk.CTkFont(size=11),
                        text_color="#aa6666",
                        anchor="w"
                    ).grid(Row=1, column=0, sticky="w", padx=16, pady=(0, 10))
        except Exception as e:
            ctk.CTkLabel(
                self.scroll_atr,
                text=f"Erro: {e}",
                text_color="#F44336"
                ).grid(pady=10)

#CARREGA TAREFAS POR PRIORIDADE AINDA PENDENTES
    def _load_prioridade(self):
        for w in self.scroll_prio.winfo_children():
            w.destroy()

        try:
            conn = get_connection()
            cur = conn.cursor(dictionary=True)

            for n in [4, 3, 2, 1]:
                cor = PRIORIDADE_COR[n]
                header = ctk.CTkFrame(self.scroll_prio, fg_color="#1a1a25", corner_radius=8)
                header.grid(sticky="ew", padx=4, pady=(8, 2))
                header.grid_columnconfigure(0, weight=1)

                ctk.CTkLabel(
                    header,
                    text=f"● {PRIORIDADE[n]}",
                    font=ctk.CTkFont(size=13,weight="bold"),
                    text_color=cor, anchor="w"
                ).grid(padx=16, pady=10, sticky="w")

                cur.execute("SELECT * FROM tarefas WHERE prioridade=%s AND ok=FALSE", (n,))
                lista = cur.fetchall()

                if not lista:
                    ctk.CTkLabel(
                        self.scroll_prio,
                        text="  Nenhuma tarefa pendente",
                        font=ctk.CTkFont(size=11),
                        text_color="#444458"
                        ).grid(sticky="w", padx=24)
                else:
                    for t in lista:
                        row = ctk.CTkFrame(self.scroll_prio, fg_color="#13131b", corner_radius=6)
                        row.grid(sticky="ew", padx=16, pady=2)
                        row.grid_columnconfigure(0, weight=1)

                        ctk.CTkLabel(
                            row,
                            text=f"  {t['titulo']}",
                            font=ctk.CTkFont(size=12),
                            text_color="#c0c0d8", anchor="w"
                        ).grid(row=0, column=0, sticky="w", padx=8, pady=8)

                        ctk.CTkLabel(row,
                                     text=t['data'].strftime('%d/%m/%Y'),
                                     font=ctk.CTkFont(size=11),
                                     text_color="#555570"
                                    ).grid(row=0, column=1, padx=12)
            conn.close()
        except Exception as e:
            ctk.CTkLabel(
                self.scroll_prio,
                text=f"Erro: {e}",
                text_color="#F44336"
            ).grid(pady=10)

#CARREGA AS ESTATISTICAS GERAL

    def _load_stats(self):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM tarefas")
            total = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE ok=TRUE")
            conc = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE ok=FALSE")
            pend = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE data < NOW() AND ok=FALSE")
            atr = cur.fetchone()[0]
            cur.execute("SELECT COUNT(*) FROM tarefas WHERE data >= NOW() AND data <= DATE_ADD(NOW(), INTERVAL 7 DAY) AND ok=FALSE")
            prox = cur.fetchone()[0]
            conn.close()

            stats = [
                ("Total de Tarefas", str(total), "#e8d5b0"),
                ("Concluídas", f"{conc}  ({conc*100//total if total else 0}%)", "#4CAF50"),
                ("Pendentes", str(pend), "#2196F3"),
                ("Atrasadas", str(atr), "#F44336"),
                ("Próximas (7d)", str(prox), "#FF9800"),
                ("Taxa de Conclusão", f"{conc*100//total if total else 0}%", "#9C27B0"),
            ]
            for i, (label, val, cor) in enumerate(stats):
                card = ctk.CTkFrame(self.stats_frame, fg_color="#17171f", corner_radius=12, height=90)
                card.grid(row=i//2, column=i%2, padx=8, pady=8, sticky="ew")
                card.grid_columnconfigure(0, weight=1)
                ctk.CTkLabel(card, text=label, font=ctk.CTkFont(size=11),
                             text_color="#666680").grid(padx=20, pady=(16, 2), sticky="w")
                ctk.CTkLabel(card, text=val, font=ctk.CTkFont("Georgia", 26, "bold"),
                             text_color=cor).grid(padx=20, pady=(0, 16), sticky="w")
        except Exception as e:
            ctk.CTkLabel(self.stats_frame, text=f"Erro: {e}", text_color="#F44336").grid(pady=10)


if __name__ == "__main__":
    try:
        inicializar_banco()
    except Exception as e:
        import sys
        print(f"Erro ao conectar ao banco: {e}")
        sys.exit(1)

    app = App()
    app.mainloop()


