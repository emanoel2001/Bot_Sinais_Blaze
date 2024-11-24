import streamlit as st
from tinydb import TinyDB, Query
import hashlib
import random
import string
import pandas as pd
import datetime
import bcrypt
import json
import os
# Criar pasta caso não tenha
if not os.path.exists("db"):
    os.makedirs("db")

# Caminho do banco de dados
DB_PATH = "db/usuarios.json"

def verificar_banco_de_dados(path):
    if not os.path.exists(path):
        st.warning("Banco de dados não encontrado. Criando...")
        with open(path, 'w') as f:
            json.dump([], f)

# Verifica e recria o banco de dados, se necessário
verificar_banco_de_dados(DB_PATH)
USER_DB_PATH_TEMPLATE = "db/{}.json"
# Inicializa o TinyDB após a verificação
db = TinyDB(DB_PATH)
user_query = Query()

# Funções auxiliares
def gerar_senha_temporaria():
    """Gera uma senha temporária aleatória de 8 caracteres"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=8))

def hash_senha(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()  # Converte para string

# Funções de autenticação
def criar_usuario(username, password, email):
    """Cria um novo usuário se o nome de usuário e e-mail não existirem"""
    password_hash = hash_senha(password)
    if db.search((user_query.username == username) | (user_query.email == email)):
        return False
    db.insert({"username": username, "password": password_hash, "email": email})
    user_db = TinyDB(USER_DB_PATH_TEMPLATE.format(username), encoding="utf-8")
    user_db.insert_multiple([])  # Cria banco de dados do usuário
    return True

def verificar_usuario(username, password):
    user = db.search(user_query.username == username)
    if user:
        stored_hash = user[0]['password'].encode()  # Converte para bytes
        if bcrypt.checkpw(password.encode(), stored_hash):
            return True
    return False

def recuperar_senha(email, nova_senha):
    """Recupera a senha do usuário e retorna uma nova senha escolhida"""
    result = db.search(user_query.email == email)
    if result:
        password_hash = hash_senha(nova_senha)
        db.update({"password": password_hash}, user_query.email == email)
        return True
    return False

# Funções de gerenciamento de clientes
class ClienteManager:
    """Classe para gerenciamento de clientes"""
    def __init__(self, db_path):
        self.db = TinyDB(db_path, encoding="utf-8")
        self.query = Query()

    def cadastrar_cliente(self, cliente):
        """Cadastra um novo cliente, se não houver duplicatas"""
        if self.db.search((self.query.Nome == cliente['Nome']) | (self.query.CPF == cliente['CPF']) | (self.query.Email == cliente['Email'])):
            return False
        self.db.insert(cliente)
        return True

    def buscar_cliente(self, nome):
        """Busca clientes pelo nome (parcial)"""
        return self.db.search(self.query.Nome.search(nome))

    def listar_clientes(self):
        """Lista todos os clientes cadastrados"""
        return self.db.all()

    def remover_cliente(self, nome):
        """Remove um cliente pelo nome"""
        self.db.remove(self.query.Nome == nome)

    def atualizar_cliente(self, nome, campo, novo_valor):
        """Atualiza informações de um cliente"""
        self.db.update({campo: novo_valor}, self.query.Nome == nome)

# Funções de gerenciamento de página no Streamlit
def main():
    """Função principal do app Streamlit"""
    st.set_page_config(page_title="Gerenciamento de Clientes", layout="wide", initial_sidebar_state="expanded")
    
    # Definir estado de login na sessão
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = ""

    if st.session_state.logged_in:
        gerenciamento_clientes()
    else:
        menu = st.sidebar.selectbox("Selecione uma opção", ["Login", "Cadastro", "Recuperação de Senha"])
        if menu == "Login":
            login()
        elif menu == "Cadastro":
            cadastro()
        elif menu == "Recuperação de Senha":
            recuperacao_senha()

def login():
    """Página de login"""
    st.title("Login")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if verificar_usuario(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Bem-vindo, {username}!")
            gerenciamento_clientes()
        else:
            st.error("Usuário ou senha incorretos.")

def cadastro():
    """Página de cadastro de novo usuário"""
    st.title("Cadastro")
    username = st.text_input("Novo Usuário")
    password = st.text_input("Nova Senha", type="password")
    confirm_password = st.text_input("Confirmar Senha", type="password")
    email = st.text_input("E-mail")

    if st.button("Cadastrar"):
        if password == confirm_password:
            if criar_usuario(username, password, email):
                st.success("Usuário cadastrado com sucesso!", icon="✅")
            else:
                st.error("Usuário ou e-mail já existem.", icon="❌")
        else:
            st.warning("As senhas não coincidem.", icon="⚠️")

def recuperacao_senha():
    """Página para recuperação de senha"""
    st.title("Recuperação de Senha")
    email = st.text_input("E-mail para recuperação")
    nova_senha = st.text_input("Nova Senha", type="password")
    confirm_nova_senha = st.text_input("Confirmar Nova Senha", type="password")
    
    if st.button("Recuperar Senha"):
        if nova_senha == confirm_nova_senha:
            if recuperar_senha(email, nova_senha):
                st.success("Senha redefinida com sucesso!")
            else:
                st.error("E-mail não encontrado.")
        else:
            st.error("As senhas não coincidem.")

def gerenciamento_clientes():
    """Página principal de gerenciamento de clientes"""
    username = st.session_state.username
    db_path = USER_DB_PATH_TEMPLATE.format(username)  # Caminho do banco de dados do usuário
    db_manager = ClienteManager(db_path)

    menu = st.sidebar.radio("Menu", ["Cadastrar Cliente", "Verificar Cliente", "Remover Cliente", "Atualizar Cliente", "Listar Clientes", "Sair"])

    if menu == "Cadastrar Cliente":
        cadastrar_cliente(db_manager)
    elif menu == "Verificar Cliente":
        verificar_cliente(db_manager)
    elif menu == "Remover Cliente":
        remover_cliente(db_manager)
    elif menu == "Atualizar Cliente":
        atualizar_cliente(db_manager)
    elif menu == "Listar Clientes":
        listar_clientes(db_manager)
    elif menu == "Sair":
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.success("Você saiu com sucesso!")
        login()

def cadastrar_cliente(db_manager):
    """Cadastro de um novo cliente"""
    with st.form("Cadastro de Cliente"):
        nome = st.text_input("Nome completo", value="", placeholder="Digite o nome completo").strip().upper()
        data_nascimento = st.date_input("Data de Nascimento", format="DD/MM/YYYY")
        endereco = st.text_input("Endereço", value="", placeholder="Digite o endereço").strip().upper()
        telefone = st.text_input("Telefone", value="", placeholder="Digite o telefone").strip()
        cpf = st.text_input("CPF", value="", placeholder="Digite o CPF").strip()
        email = st.text_input("E-mail", value="", placeholder="Digite o e-mail")

        submit_button = st.form_submit_button("Cadastrar")
        if submit_button:
            if nome and data_nascimento and endereco and telefone and cpf and email:
                cliente = {
                    "Nome": nome,
                    "DataNascimento": str(data_nascimento),
                    "Endereco": endereco,
                    "Telefone": telefone,
                    "CPF": cpf,
                    "Email": email
                }
                if db_manager.cadastrar_cliente(cliente):
                    st.success("Cliente cadastrado com sucesso!")
                else:
                    st.error("Cliente com os mesmos dados já cadastrado.")
            else:
                st.warning("Todos os campos são obrigatórios.")

def verificar_cliente(db_manager):
    """Verificar se um cliente existe"""
    nome = st.text_input("Nome do cliente para verificar").strip().upper()
    if st.button("Buscar Cliente"):
        resultado = db_manager.buscar_cliente(nome)
        if resultado:
            for cliente in resultado:
                st.write(f"**Nome**: {cliente['Nome']}")
                st.write(f"**Data de Nascimento**: {cliente['DataNascimento']}")
                st.write(f"**Endereço**: {cliente['Endereco']}")
                st.write(f"**Telefone**: {cliente['Telefone']}")
                st.write(f"**CPF**: {cliente['CPF']}")
                st.write(f"**E-mail**: {cliente['Email']}")
        else:
            st.error("Cliente não encontrado.")

def remover_cliente(db_manager):
    """Remover um cliente"""
    nome = st.text_input("Nome do cliente para remover").strip().upper()
    if st.button("Remover Cliente"):
        db_manager.remover_cliente(nome)
        st.success(f"Cliente {nome} removido com sucesso!")

def atualizar_cliente(db_manager):
    """Atualizar dados de um cliente"""
    nome = st.text_input("Nome do cliente para atualizar").strip().upper()
    if st.button("Buscar Cliente"):
        cliente = db_manager.buscar_cliente(nome)
        if cliente:
            campo_atualizado = st.selectbox("Campo a ser atualizado", ["Nome", "DataNascimento", "Endereco", "Telefone", "CPF", "Email"])
            novo_valor = st.text_input(f"Novo valor para {campo_atualizado}")
            if st.button("Atualizar Cliente"):
                db_manager.atualizar_cliente(nome, campo_atualizado, novo_valor)
                st.success(f"{campo_atualizado} do cliente atualizado com sucesso!")
        else:
            st.error("Cliente não encontrado.")

def listar_clientes(db_manager):
    """Listar todos os clientes cadastrados"""
    clientes = db_manager.listar_clientes()
    if clientes:
        df = pd.DataFrame(clientes)
        st.dataframe(df.style.set_table_styles([{
            'selector': 'thead th',
            'props': [('background-color', '#4CAF50'), ('color', 'white')]
        }]))
    else:
        st.write("Nenhum cliente cadastrado.")

if __name__ == "__main__":
    main()
# executar o streamlit: streamlit run main.py --server.enableCORS false --server.enableXsrfProtection false
