import streamlit as st
import psycopg2
from datetime import datetime, date, timedelta
import pandas as pd

# ─────────────────────────────────────────────────────
# CONFIGURAÇÃO — edite conforme seu ambiente
# ─────────────────────────────────────────────────────
CONFIG = {
    "host":     "localhost",        # IP do servidor ou "localhost"
    "port":     5432,
    "database": "tarefas_academicas",
    "user":     "postgres",
    "password": "sua_senha_aqui"
}

PRIORIDADE = {1: "🟢 Baixa", 2: "🔵 Média", 3: "🟠 Alta", 4: "🔴 Urgente"}
PRIORIDADE_COR = {1: "#4caf50", 2: "#2196f3", 3: "#ff9800", 4: "#f44336"}

# ─────────────────────────────────────────────────────
# BANCO DE DADOS
# ─────────────────────────────────────────────────────

def conectar():
    try:
        return psycopg2.connect(**CONFIG)
    except psycopg2.OperationalError as e:
        st.error(f"❌ Erro ao conectar ao banco: {e}")
        st.stop()

def criar_tabela():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id           SERIAL PRIMARY KEY,
            titulo       TEXT    NOT NULL,
            descricao    TEXT,
            disciplina   TEXT    NOT NULL,
            prioridade   INTEGER NOT NULL CHECK (prioridade BETWEEN 1 AND 4),
            data_entrega DATE    NOT NULL,
            concluida    BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def buscar_tarefas(filtro_status=None, filtro_disciplina=None):
    conn = conectar()
    cursor = conn.cursor()
    query = "SELECT * FROM tarefas WHERE 1=1"
    params = []
    if filtro_status == "Pendentes":
        query += " AND concluida = FALSE"
    elif filtro_status == "Concluídas":
        query += " AND concluida = TRUE"
    if filtro_disciplina and filtro_disciplina != "Todas":
        query += " AND disciplina = %s"
        params.append(filtro_disciplina)
    query += " ORDER BY prioridade DESC, data_entrega"
    cursor.execute(query, params)
    tarefas = cursor.fetchall()
    cursor.close()
    conn.close()
    return tarefas

def buscar_disciplinas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT disciplina FROM tarefas ORDER BY disciplina")
    discs = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return discs

def inserir_tarefa(titulo, descricao, disciplina, prioridade, data_entrega):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO tarefas (titulo, descricao, disciplina, prioridade, data_entrega)
        VALUES (%s, %s, %s, %s, %s)
    """, (titulo, descricao, disciplina, prioridade, data_entrega))
    conn.commit()
    cursor.close()
    conn.close()

def atualizar_tarefa(id_, titulo, prioridade, concluida):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tarefas SET titulo=%s, prioridade=%s, concluida=%s WHERE id=%s
    """, (titulo, prioridade, concluida, id_))
    conn.commit()
    cursor.close()
    conn.close()

def excluir_tarefa(id_):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tarefas WHERE id=%s", (id_,))
    conn.commit()
    cursor.close()
    conn.close()

def buscar_stats():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tarefas")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tarefas WHERE concluida=TRUE")
    conc = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tarefas WHERE data_entrega < CURRENT_DATE AND concluida=FALSE")
    atr = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM tarefas WHERE data_entrega BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '7 days' AND concluida=FALSE")
    prox = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return total, conc, atr, prox

# ─────────────────────────────────────────────────────
# INTERFACE STREAMLIT
# ─────────────────────────────────────────────────────

st.set_page_config(
    page_title="Gestão de Tarefas Acadêmicas",
    page_icon="📚",
    layout="wide"
)

# CSS customizado
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }

    .main { background-color: #0f1117; }

    .header-title {
        font-size: 2.2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0;
    }

    .header-sub {
        color: #888;
        font-size: 0.9rem;
        margin-top: 0;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
    }

    .metric-label {
        color: #888;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.3rem;
    }

    .tarefa-card {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 0.8rem;
        border-left: 4px solid;
        transition: transform 0.2s;
    }

    .tarefa-card:hover { transform: translateX(4px); }

    .tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        margin-right: 6px;
    }

    .stButton > button {
        border-radius: 8px;
        font-family: 'Sora', sans-serif;
        font-weight: 600;
    }

    div[data-testid="stForm"] {
        background: #1a1d27;
        border: 1px solid #2a2d3a;
        border-radius: 12px;
        padding: 1.5rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #ccc;
        border-bottom: 1px solid #2a2d3a;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização
criar_tabela()

# ─── CABEÇALHO ───
st.markdown('<p class="header-title">📚 Gestão de Tarefas Acadêmicas</p>', unsafe_allow_html=True)
st.markdown('<p class="header-sub">// sistema integrado com PostgreSQL via rede local</p>', unsafe_allow_html=True)
st.divider()

# ─── MÉTRICAS ───
total, conc, atr, prox = buscar_stats()
pendentes = total - conc
pct = int(conc * 100 / total) if total > 0 else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#667eea">{total}</div>
        <div class="metric-label">Total de Tarefas</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#4caf50">{conc}</div>
        <div class="metric-label">Concluídas ({pct}%)</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#f44336">{atr}</div>
        <div class="metric-label">Atrasadas</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#ff9800">{prox}</div>
        <div class="metric-label">Vencem em 7 dias</div>
    </div>""", unsafe_allow_html=True)

st.divider()

# ─── ABAS ───
aba1, aba2, aba3 = st.tabs(["📋 Tarefas", "➕ Nova Tarefa", "✏️ Gerenciar"])

# ══════════════════════════════════
# ABA 1 — LISTAR TAREFAS
# ══════════════════════════════════
with aba1:
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        filtro_status = st.selectbox("Status", ["Todas", "Pendentes", "Concluídas"])
    with col_f2:
        disciplinas = ["Todas"] + buscar_disciplinas()
        filtro_disc = st.selectbox("Disciplina", disciplinas)

    tarefas = buscar_tarefas(filtro_status, filtro_disc)

    if not tarefas:
        st.info("Nenhuma tarefa encontrada com os filtros selecionados.")
    else:
        for t in tarefas:
            id_, titulo, desc, disc, pri, data_e, ok = t
            dias = (data_e - date.today()).days
            cor = PRIORIDADE_COR[pri]

            if ok:
                status_txt = "✅ Concluída"
                status_cor = "#4caf50"
            elif dias < 0:
                status_txt = f"⚠️ Atrasada {abs(dias)}d"
                status_cor = "#f44336"
            elif dias <= 7:
                status_txt = f"⏰ {dias} dias"
                status_cor = "#ff9800"
            else:
                status_txt = f"📅 {dias} dias"
                status_cor = "#888"

            st.markdown(f"""
            <div class="tarefa-card" style="border-left-color:{cor}">
                <div style="display:flex; justify-content:space-between; align-items:center">
                    <div>
                        <strong style="font-size:1rem; color:#eee">{titulo}</strong>
                        <span class="tag" style="background:{cor}22; color:{cor}">{PRIORIDADE[pri]}</span>
                        <span class="tag" style="background:#ffffff11; color:#aaa">{disc}</span>
                    </div>
                    <span style="color:{status_cor}; font-family:'JetBrains Mono',monospace; font-size:0.85rem; font-weight:600">{status_txt}</span>
                </div>
                {"<p style='color:#666; font-size:0.85rem; margin-top:0.4rem; margin-bottom:0'>"+desc+"</p>" if desc else ""}
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════
# ABA 2 — NOVA TAREFA
# ══════════════════════════════════
with aba2:
    st.markdown('<div class="section-title">Cadastrar Nova Tarefa</div>', unsafe_allow_html=True)
    with st.form("form_nova_tarefa", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            titulo     = st.text_input("Título *", placeholder="Ex: Trabalho de Cálculo")
            disciplina = st.text_input("Disciplina *", placeholder="Ex: Cálculo I")
        with col2:
            prioridade   = st.selectbox("Prioridade *", options=[1, 2, 3, 4],
                                        format_func=lambda x: PRIORIDADE[x])
            data_entrega = st.date_input("Data de Entrega *",
                                         min_value=date.today(),
                                         value=date.today() + timedelta(days=7))
        descricao = st.text_area("Descrição", placeholder="Detalhes da tarefa (opcional)")

        submitted = st.form_submit_button("✅ Cadastrar Tarefa", use_container_width=True)
        if submitted:
            if not titulo or not disciplina:
                st.error("Título e Disciplina são obrigatórios!")
            else:
                inserir_tarefa(titulo, descricao, disciplina, prioridade, data_entrega)
                st.success(f"Tarefa **{titulo}** cadastrada com sucesso!")
                st.rerun()

# ══════════════════════════════════
# ABA 3 — GERENCIAR (EDITAR/EXCLUIR)
# ══════════════════════════════════
with aba3:
    tarefas_todas = buscar_tarefas()
    if not tarefas_todas:
        st.info("Nenhuma tarefa cadastrada ainda.")
    else:
        opcoes = {f"[ID {t[0]}] {t[1]} — {t[3]}": t for t in tarefas_todas}
        escolha = st.selectbox("Selecione uma tarefa", list(opcoes.keys()))
        t = opcoes[escolha]
        id_, titulo, desc, disc, pri, data_e, ok = t

        col_ed, col_del = st.columns([3, 1])

        with col_ed:
            st.markdown('<div class="section-title">Editar Tarefa</div>', unsafe_allow_html=True)
            with st.form("form_editar"):
                novo_titulo = st.text_input("Título", value=titulo)
                nova_pri    = st.selectbox("Prioridade", options=[1, 2, 3, 4],
                                           index=pri - 1,
                                           format_func=lambda x: PRIORIDADE[x])
                novo_ok     = st.checkbox("Marcar como concluída", value=ok)
                if st.form_submit_button("💾 Salvar Alterações", use_container_width=True):
                    atualizar_tarefa(id_, novo_titulo, nova_pri, novo_ok)
                    st.success("Tarefa atualizada!")
                    st.rerun()

        with col_del:
            st.markdown('<div class="section-title">Excluir</div>', unsafe_allow_html=True)
            st.warning(f"**{titulo}**")
            if st.button("🗑️ Excluir Tarefa", use_container_width=True, type="primary"):
                excluir_tarefa(id_)
                st.success("Tarefa excluída!")
                st.rerun()
