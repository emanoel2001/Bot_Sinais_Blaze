import streamlit as st
import csv
import os

# Função para verificar se o usuário já existe
def verificar_usuario(usuario, senha):
    if not os.path.exists("clientes.csv"):
        return False  # Caso o arquivo não exista, retorna False
    
    try:
        with open("clientes.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.reader(arquivo)
            for linha in leitor:
                # Agora esperamos que os campos sejam: [nome, email, usuario, senha]
                if linha[2] == usuario and linha[3] == senha:
                    return True
    except Exception as e:
        st.error(f"Erro ao verificar usuário: {e}")
    return False

# Tela de login
def tela_login():
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.subheader("👤 Login")
        
        usuario = st.text_input("Digite seu usuário")
        senha = st.text_input("Digite sua senha", type="password")
        login = st.button("Login")
        
        if login:
            if not usuario or not senha:
                st.error("⚠ Preencha todos os campos!")
            else:
                if verificar_usuario(usuario, senha):
                    st.success("✅ Login realizado com sucesso!")
                    st.session_state["logged_in"] = True
                else:
                    st.error("❌ Usuário ou senha incorretos. Tente novamente!")
    else:
        st.success("Você já está logado!")
