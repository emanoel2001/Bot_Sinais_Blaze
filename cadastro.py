import streamlit as st
import csv

# Função para verificar se o usuário já existe
def verificar_usuario(usuario, senha):
    try:
        with open("clientes.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                if (linha['Usuário'] == usuario and linha['Senha'] == senha):
                    return True
    except FileNotFoundError:
        pass
    return False

def tela_cadastro():
    st.subheader("📰 Cadastro")

    nome = st.text_input("Digite seu nome")
    email = st.text_input("Digite seu email")
    usuario = st.text_input("Digite seu usuário")
    senha = st.text_input("Digite sua senha", type="password")
    cadastrar = st.button("Cadastrar")

    if cadastrar:
        if not nome or not email or not usuario or not senha:
            st.error("⚠ Todos os campos são obrigatórios!")
        else:
            with open("clientes.csv", "a", newline="", encoding="utf-8") as arquivo:
                campos = ["Nome", "E-mail", "Usuário", "Senha"]
                escritor = csv.DictWriter(arquivo, fieldnames=campos)
                escritor.writerow({"Nome": nome, "E-mail": email, "Usuário": usuario, "Senha": senha})
            st.success("✅ Cadastro realizado com sucesso!")