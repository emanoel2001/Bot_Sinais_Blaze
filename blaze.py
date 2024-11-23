from time import sleep
import requests
import streamlit as st

def robo_blaze():
    st.subheader("Bem-vindo ao robô da blaze (Double)")
    sair = st.button("Sair")
    
    # Verifica se o botão "Sair" foi clicado
    if sair:
        st.session_state["logged_in"] = False
        st.success("Você saiu do sistema!")
    else:
        st.session_state["logged_in"] = True

        # CSS para os quadrados
        st.markdown("""
        <style>
        .quadrado {
            display: inline-block;
            width: 50px;
            height: 50px;
            margin: 5px;
            text-align: center;
            line-height: 50px;
            font-weight: bold;
            color: white;
            border-radius: 5px;
        }
        .verde { background-color: green; }
        .preto { background-color: black; }
        .branco { background-color: gray; color: black; }
        </style>
        """, unsafe_allow_html=True)

        # Elemento dinâmico para a lista de resultados
        result_placeholder = st.empty()
        
        # Lista para armazenar todos os resultados
        resultados = []
        
        while st.session_state.get("logged_in", False):
            try:
                sleep(1.4)  # Delay entre as requisições
                
                # Fazendo a requisição para a API
                data_double = requests.get('https://blaze1.space/api/singleplayer-originals/originals/roulette_games/recent/1')
                resp_double = data_double.json()

                # Pegando o último resultado
                ultimo_resultado = resp_double[0]['roll']
                
                # Adiciona o novo valor apenas se ele for diferente do último valor
                if not resultados or ultimo_resultado != resultados[0]:
                    resultados.insert(0, ultimo_resultado)

                    # Criando o HTML para exibir todos os resultados com as cores
                    html = ""
                    for resultado in resultados:
                        if 1 <= resultado <= 7:
                            cor = "verde"  # Verde
                        elif 8 <= resultado <= 14:
                            cor = "preto"  # Preto
                        else:
                            cor = "branco"  # Branco

                        html += f'<div class="quadrado {cor}">{resultado}</div>'
                    
                    # Atualizando o placeholder com todos os resultados
                    result_placeholder.markdown(html, unsafe_allow_html=True)
    
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
