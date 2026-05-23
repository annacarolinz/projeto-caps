import streamlit as st
import pandas as pd
import sqlite3

# --- FUNÇÕES DO BANCO DE DADOS ---
def criar_tabela():
    conn = sqlite3.connect('dados_caps.db')
    c = conn.cursor()
    # Cria a tabela se ela não existir
    c.execute('''CREATE TABLE IF NOT EXISTS evolucao 
                 (nome TEXT, humor INTEGER, autonomia INTEGER, data DATE)''')
    conn.commit()
    conn.close()

def salvar_dados(nome, humor, autonomia):
    conn = sqlite3.connect('dados_caps.db')
    c = conn.cursor()
    # Insere os dados (adicionando a data atual automaticamente)
    c.execute("INSERT INTO evolucao (nome, humor, autonomia, data) VALUES (?, ?, ?, date('now'))", 
              (nome, humor, autonomia))
    conn.commit()
    conn.close()

def carregar_dados():
    conn = sqlite3.connect('dados_caps.db')
    df = pd.read_sql_query("SELECT * FROM evolucao", conn)
    conn.close()
    return df

# --- INTERFACE ---
st.title("Monitoramento CAPS - Sistema de Prontuário")

# Inicializa o banco de dados
criar_tabela()

st.sidebar.header("Novo Registro")
nome_usuario = st.sidebar.text_input("Nome do Usuário")
nivel_humor = st.sidebar.slider("Humor", 0, 10, 5)
nivel_autonomia = st.sidebar.slider("Autonomia", 0, 10, 5)

if st.sidebar.button("Salvar no Histórico"):
    if nome_usuario:
        salvar_dados(nome_usuario, nivel_humor, nivel_autonomia)
        st.sidebar.success(f"Registro de {nome_usuario} salvo!")
    else:
        st.sidebar.error("Por favor, digite o nome do usuário.")

# --- VISUALIZAÇÃO DOS DADOS SALVOS ---
st.write("### Histórico de Evolução (Banco de Dados)")
dados = carregar_dados()

if not dados.empty:
    # Mostra a tabela de dados
    st.dataframe(dados)
    
    # Gráfico simples baseado no que está no banco
    st.write("### Análise de Tendência")
    st.line_chart(dados.set_index('data')[['humor', 'autonomia']])
else:
    st.info("Ainda não há dados salvos no histórico.")
