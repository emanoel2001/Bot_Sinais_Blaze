import streamlit as st
import csv
from login import tela_login
from cadastro import tela_cadastro
from blaze import robo_blaze
import base64

# Configuração global da página (deve ser o primeiro comando no arquivo principal)
st.set_page_config(page_icon="flash.jpg", page_title="FlashBot")

# Função para verificar se o usuário já existe
def verificar_usuario(usuario, senha):
    try:
        with open("clientes.csv", "r", encoding="utf-8") as arquivo:
            leitor = csv.DictReader(arquivo)
            for linha in leitor:
                if linha['Usuário'] == usuario and linha['Senha'] == senha:
                    return True
    except FileNotFoundError:
        pass
    return False

# Inicialização do estado
if "menu" not in st.session_state:
    st.session_state["menu"] = "👤 Login"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Configuração do menu lateral
menu = st.sidebar.radio("📜 Menu", ["👤 Login", "📰 Cadastrar-se", "🤖 Robô Blaze"], 
                        index=["👤 Login", "📰 Cadastrar-se", "🤖 Robô Blaze"].index(st.session_state["menu"]))

st.session_state["menu"] = menu  # Atualiza o estado do menu selecionado

# # Função para adicionar uma imagem de fundo com transparência
# def adicionar_fundo(imagem_path, opacidade=0.2):
#     with open(imagem_path, "rb") as imagem:
#         base64_imagem = base64.b64encode(imagem.read()).decode()
#     st.markdown(
#         f"""
#         <style>
#         .stApp {{
#             background: linear-gradient(rgba(255, 255, 255, {opacidade}), rgba(255, 255, 255, {opacidade})), 
#                         url("data:image/jpeg;base64,{base64_imagem}");
#             background-size: 1;
#             background-position: center;
#             background-repeat: no-repeat;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# Adicionar a imagem de fundo com opacidade ajustável (0.5 é 50% transparente)
# adicionar_fundo("flash.jpg", opacidade=0.2)

# Navegação pelas páginas
if menu == "👤 Login":
    tela_login()
elif menu == "📰 Cadastrar-se":
    tela_cadastro()
elif menu == "🤖 Robô Blaze":
    if st.session_state["logged_in"]:
        robo_blaze()
    else:
        st.warning("⚠ Você precisa estar logado para acessar o Robô!")
        st.info("Faça login na aba '👤 Login'.")
else:
    st.subheader("🏠 Bem-vindo ao sistema FlashBot!")
