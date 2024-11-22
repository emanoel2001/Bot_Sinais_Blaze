from datetime import datetime
import requests
from time import sleep
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import json
from pagamento import Payload

# Variaveis globais
p = Payload('Carlos Sousa', '+5585992354262', '10.00', 'FORTALEZA', 'AJUDA BOT')
p.gerarPayload()
hora = datetime.now().strftime("%H")
minuto = datetime.now().strftime("%M")
hora_atual = int(hora)
minuto_atual = int(minuto)
bot = telebot.TeleBot(token="8135881321:AAHGwJKETQg22FIJ2Yt3PHEkkpFoQyLGjo8")
chat_id = '-1002346722956'
estrategias_info = {}
ultima_mensagem_id = None
ultima_mensagem_id_branco = None
ultima_mensagem_id_loss = None
ultima_mensagem_id_photo = None
aposta = None
# gunicorn main.wsgi
id_ = None
estrategias = None
check = []
zero = True
iniciar = True
entrada = None
green = False
red = False
gale = 0
max_gale = 2
vitoria_seguida = 0
win = 0
branco = 0
sg = 0
g1 = 0
g2 = 0
bsg = 0
bg1 = 0
bg2 = 0
loss = 0

def salvar_estrategias_info():
    # Ordena as estratégias pelo ID (converte as chaves para int para garantir a ordenação correta)
    estrategias_ordenadas = {k: estrategias_info[k] for k in sorted(estrategias_info, key=int)}
    with open("analisador.json", "w") as arquivo:
        json.dump(estrategias_ordenadas, arquivo, indent=4)

def atualizar_estrategia_info(id_, resultado):
    global estrategias_info

    # Inicializa a estratégia se ela não existir
    if id_ not in estrategias_info:
        estrategias_info[id_] = {"WIN_SG": 0, "WIN_G1": 0, "WIN_G2": 0, "LOSS": 0, "BRANCOS_SG": 0, "BRANCOS_G1": 0, "BRANCOS_G2": 0}

    # Atualiza os valores com base no resultado
    if resultado == "WIN_SG":
        estrategias_info[id_]["WIN_SG"] += 1
    elif resultado == "WIN_G1":
        estrategias_info[id_]["WIN_G1"] += 1
    elif resultado == "WIN_G2":
        estrategias_info[id_]["WIN_G2"] += 1
    elif resultado == "LOSS":
        estrategias_info[id_]["LOSS"] += 1
    elif resultado == "BRANCO_SG":
        estrategias_info[id_]["BRANCOS_SG"] += 1
    elif resultado == "BRANCO_G1":
        estrategias_info[id_]["BRANCOS_G1"] += 1
    elif resultado == "BRANCO_G2":
        estrategias_info[id_]["BRANCOS_G2"] += 1

    # Salva as estratégias ordenadas no arquivo
    salvar_estrategias_info()

def alerta_entrada(id_):
    
    global bot
    
    msg = bot.send_message(chat_id=chat_id, text=f'''
🚨 ALERTA DE SINAL 🚨
''')
    sleep(18)
    bot.delete_message(chat_id=chat_id, message_id=msg.message_id)
    
    return

def entrada_aposta(resultado, aposta):
    
    global bot, id_, estrategias
    
    # Criando os botões
    button_1 = InlineKeyboardButton("🎮 JOGAR", url="https://blaze1.space/pt/games/double")
    button_2 = InlineKeyboardButton("📝 CADASTRE-SE", url="https://blaze-codigo.com/r/JlZ0DV")
    button_3 = InlineKeyboardButton("💬 SUPORTE", url="https://t.me/AutoFLashB")
        
    # Criando o markup com os botões
    markup = InlineKeyboardMarkup(row_width=2)  # row_width=2 coloca os botões na mesma linha
    markup.add(button_1, button_2, button_3)
    
    if aposta == "P":
        bot.send_message(chat_id=chat_id, text=f'''
🚨 ENTRADA CONFIRMADA

🎰 ENTRAR NO (⚫️)
⚪️ PROTEJA O BRANCO
👉 APÓS ( {resultado[0]} | {"🔴" if resultado[0] >= 1 and resultado[0] <= 7 else "⚫️" if resultado[0] >= 8 and resultado[0] <= 14 else "⚪️"})
🆔: {id_}
''',reply_markup=markup)
    elif aposta == "V":
        bot.send_message(chat_id=chat_id, text=f'''
🚨 ENTRADA CONFIRMADA

🎰 ENTRAR NO (🔴)
⚪️ PROTEJA O BRANCO
👉 APÓS ( {resultado[0]} | {"🔴" if resultado[0] >= 1 and resultado[0] <= 7 else "⚫️" if resultado[0] >= 8 and resultado[0] <= 14 else "⚪️"})
🆔: {id_}
''',reply_markup=markup) 
    
    return
 
def horario():
    global hora_atual, minuto_atual, vitoria_seguida, sg, g1, g2, bsg, bg1, bg2, loss, win, branco

    # Função para resetar as variáveis
    def resetar_variaveis():
        global vitoria_seguida, win, branco, sg, g1, g2, bsg, bg1, bg2, loss
        vitoria_seguida = 0
        win = 0
        branco = 0
        sg = 0
        g1 = 0
        g2 = 0
        bsg = 0
        bg1 = 0
        bg2 = 0
        loss = 0

    # Definir os horários e as mensagens
    horarios = [
        (0, 0, "INICIANDO PARA DIA ☀️"),
        (12, 0, "INICIANDO PARA TARDE 🌅"),
        (18, 0, "INICIANDO PARA NOITE 🌙")
    ]

    # Verificar se o horário atual corresponde a algum dos horários definidos
    for h, m, mensagem in horarios:
        if hora_atual == h and minuto_atual == m:
            bot.send_message(chat_id=chat_id, text=mensagem)
            resetar_variaveis()
            break

def seguido_vitoria():
    global bot, vitoria_seguida, ultima_mensagem_id_photo
    
    # Verifica se vitoria_seguida é múltiplo de 5
    if vitoria_seguida % 5 == 0:
        caminho_foto = 'pixqrcode.png'
        if vitoria_seguida == 10:
            bot.send_sticker(chat_id=chat_id, sticker="CAACAgEAAxkBAAENLbtnPd3rbOXWjWbw5ub2WQAB8b0KJuQAAi4BAAJJ7FFEndRoL4WkwCo2BA")
        texto = bot.send_photo(chat_id=chat_id, photo=open(caminho_foto, 'rb'), caption="00020126360014br.gov.bcb.pix0114+5585992354262520400005303986540410.05802BR5912Carlos Sousa6009FORTALEZA62120508AJUDABOT63042ED9")
        
        # Se uma mensagem anterior foi enviada, tenta excluí-la
        if ultima_mensagem_id_photo is not None:
            bot.delete_message(chat_id=chat_id, message_id=ultima_mensagem_id_photo)
        
        # Envia a nova mensagem e armazena seu ID
        nova_mensagem = bot.send_message(chat_id=chat_id, text=texto)
        ultima_mensagem_id_photo = nova_mensagem.message_id
        return

def placar():
    global bot, vitoria_seguida, sg, g1, g2, bsg, bg1, bg2, loss, gale, zero, branco, ultima_mensagem_id

    if (win + branco + loss) != 0:
        b = win + branco
        a = (b / (win + branco + loss)) * 100
    else:
        a = 0
    acertividade = f"{a:.2f}%"

    # Monta a mensagem a ser enviada
    if gale == 0:
        sg += 1
        texto = f"🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n✅✅ WIN SEM GALE ✅✅\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "WIN_SG")
    elif gale == 1:
        g1 += 1
        texto = f"🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n✅✅ WIN GALE 1 ✅✅\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "WIN_G1")
    elif gale == 2:
        g2 += 1
        texto = f"🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n✅✅ WIN GALE 2 ✅✅\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "WIN_G2")
    
    # Apaga a mensagem anterior, se houver
    if ultima_mensagem_id is not None:
        bot.delete_message(chat_id=chat_id, message_id=ultima_mensagem_id)


    # Envia a nova mensagem e armazena seu ID
    nova_mensagem = bot.send_message(chat_id=chat_id, text=texto)
    ultima_mensagem_id = nova_mensagem.message_id

    return

def placar_branco():
    global bot, vitoria_seguida, sg, g1, g2, bsg, bg1, bg2, loss, gale, zero, branco, ultima_mensagem_id_branco
    
    if (win + branco + loss) != 0:
        b = win + branco
        a = (b / (win + branco + loss)) * 100
    else:
        a = 0
    acertividade = f"{a:.2f}%"

    # Monta a mensagem a ser enviada
    if gale == 0:
        bsg += 1
        texto = f"⚪️ BRANCO\n\n🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n⚪️⚪️ BRANCO SEM GALE ⚪️⚪️\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "BRANCO_SG")
    elif gale == 1:
        bg1 += 1
        texto = f"⚪️ BRANCO\n\n🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n⚪️⚪️ BRANCO GALE 1 ⚪️⚪️\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "BRANCO_G1")
    elif gale == 2:
        bg2 += 1
        texto = f"⚪️ BRANCO\n\n🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n⚪️⚪️ BRANCO GALE 2 ⚪️⚪️\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
        atualizar_estrategia_info(id_, "BRANCO_G2")
    
    # Apaga a mensagem anterior, se houver
    if ultima_mensagem_id_branco is not None:
        bot.delete_message(chat_id=chat_id, message_id=ultima_mensagem_id_branco)

    # Envia a nova mensagem e armazena seu ID
    nova_mensagem = bot.send_message(chat_id=chat_id, text=texto)
    ultima_mensagem_id_branco = nova_mensagem.message_id
        
    return

def placar_loss():
    global bot, vitoria_seguida, sg, g1, g2, bsg, bg1, bg2, loss, gale, zero, branco, ultima_mensagem_id_loss
    
    if (win + branco + loss) != 0:
        b = win + branco
        a = (b / (win + branco + loss)) * 100
    else:
        a = 0
    acertividade = f"{a:.2f}%"
    
    # Monta a mensagem a ser enviada
    texto = f"❌ LOSS\n\n🏆 Vitória(s) Seguida(s): {vitoria_seguida}\n\n❌❌ LOSS ❌❌\n\n✅ VITÓRIAS\nSG:{sg} | G1: {g1} | G2: {g2}\n❌ DERROTAS\nLOSS: {loss}\n⚪️ BRANCO\nSG: {bsg} | G1: {bg1} | G2: {bg2}\n\nACERTIVIDADE: {acertividade}"
    
    # Apaga a mensagem anterior, se houver
    if ultima_mensagem_id_loss is not None:
        bot.delete_message(chat_id=chat_id, message_id=ultima_mensagem_id_loss)

    
    # Envia a nova mensagem e armazena seu ID
    nova_mensagem = bot.send_message(chat_id=chat_id, text=texto)
    ultima_mensagem_id_loss = nova_mensagem.message_id

    
    atualizar_estrategia_info(id_, "LOSS")
        
    return

def estrategia(resultado, cor):
    global entrada, max_gale, gale, green, red, iniciar, vitoria_seguida, bot, chat_id, sg, g1, g2, loss, win, zero, branco
    global id_, estrategias, aposta

    def interpretar_cor(num):
        """Associa números com as cores: 1-7 -> 'V', 8-14 -> 'P', 0 -> 'B'"""
        if num == 0:
            return 'B'
        elif num >= 1 and num <= 7:
            return 'V'
        elif num >= 8 and num <= 14:
            return 'P'
        return None

    def obter_hora_atual():
        """Retorna a hora e o minuto atual no formato HH:MM"""
        agora = datetime.now()
        return f"{agora.hour:02}:{agora.minute:02}"

    if len(resultado) and len(cor) != 0:

        if iniciar:
            # Ler as estratégias do arquivo
            with open("estrategias_blaze_double.txt", "r") as arquivo:
                linhas = arquivo.readlines()

            # Obter o horário atual
            horario_atual = obter_hora_atual()

            # Processar cada linha das estratégias
            for linha in linhas:
                linha = linha.strip()  # Remove espaços extras e quebras de linha
                if not linha:  # Ignora linhas vazias
                    continue

                # Dividir a linha em partes (ID=ESTRATÉGIA=APOSTA)
                partes = linha.split("=")
                if len(partes) != 3:  # Valida a estrutura esperada (ID=ESTRATÉGIA=APOSTA)
                    continue

                id_ = partes[0].strip()  # Ex: "52"
                estrategia = partes[1][::-1].strip()  # Ex: "13:22"
                aposta = partes[2].strip()  # Ex: "P"
            
                # Verificar se a estratégia está baseada em horário
                if ":" in estrategia:  # Se for uma estratégia baseada em horário
                    if estrategia == horario_atual:  # Verifica se o horário corresponde
                        entrada_aposta(resultado, aposta)  # Função para realizar a aposta
                        iniciar = False
                        green = True
                        break  # Encerra o loop após a aposta
                    else:
                        continue  # Se o horário não coincidir, pula para a próxima estratégia
                else:
                    # Caso a estratégia tenha números e cores misturados (como "5-14-7-V-P")
                    estrategia_convertida = []
                    estrategia_itens = estrategia.split("-")

                    # Verificar se a estratégia está corretamente estruturada
                    estrategia_valida = True
                    for item in estrategia_itens:
                        if item.isdigit():  # Se for um número, verifica se está na lista resultado
                            num = int(item)
                            if num not in resultado:
                                estrategia_valida = False
                                break
                        elif item in ['V', 'P', 'B']:  # Se for uma cor, verifica se está na lista cor
                            if item not in cor:
                                estrategia_valida = False
                                break
                        else:
                            estrategia_valida = False
                            break
                    
                    # Se a estratégia for válida, comparando os números e cores
                    if estrategia_valida:
                        # Verificar se as cores e os números coincidem nas posições corretas
                        estrategia_convertida = []
                        for item in estrategia_itens:
                            if item.isdigit():  # Verifica se o item é um número
                                num_int = int(item)
                                cor_associada = interpretar_cor(num_int)
                                estrategia_convertida.append(cor_associada)
                            else:
                                estrategia_convertida.append(item)  # Adiciona a cor diretamente

                        # Agora verificamos se tanto os números quanto as cores coincidem
                        cor_completa = [interpretar_cor(num) for num in resultado]
                        if cor_completa[:len(estrategia_convertida)] == estrategia_convertida:
                            # print(f"id: {id_} estrategia: {estrategia} | {estrategia_convertida} Aposta: {aposta}")
                            entrada_aposta(resultado, aposta)  # Função para realizar a aposta
                            iniciar = False
                            green = True
                            break  # Encerra o loop após a aposta
                        elif cor_completa[:len(estrategia_convertida) - 1] == estrategia_convertida[:len(estrategia_convertida) - 1]:
                            alerta_entrada(id_)  # Caso as cores e números não coincidam, alerta

        elif iniciar == False:  # Quando iniciar for False, processa o bloco de apostas
            if cor[0] == aposta and green == True:
                vitoria_seguida += 1
                win += 1
                try:
                    bot.send_message(chat_id=chat_id, text=f"✅ VITÓRIA")
                except:                    
                    pass
                placar()
                seguido_vitoria()
                gale = 0
                green = False
                iniciar = True  # Após uma vitória, reinicia a estratégia

            elif cor[0] == "B" and green == True and zero == True:
                vitoria_seguida += 1
                branco += 1
                try:
                    bot.send_message(chat_id=chat_id, text=f"⚪️ BRANCO")
                except:
                    pass

                placar_branco()
                gale = 0
                green = False
                iniciar = True  # Após uma vitória, reinicia a estratégia

            elif cor[0] != aposta and gale <= max_gale:
                if gale < max_gale:
                    gale += 1
                    ms1 = bot.send_message(chat_id=chat_id, text=f"\n⚠️ Vamos para o {gale} gale")
                    sleep(15)
                    bot.delete_message(chat_id=chat_id, message_id=ms1.message_id)
                else:
                    loss += 1
                    try:
                        bot.send_message(chat_id=chat_id, text=f"❌ LOSS")
                    except:
                        pass
                    
                    placar_loss()
                    gale = 0
                    vitoria_seguida = 0
                    iniciar = True
                    green = False
    
    else:
        pass
    
# print(f"id: {id_} estrategia: {estrategia} | {estrategia_convertida} Aposta: {aposta}")

def main():
    p = Payload('Carlos Sousa', '+5585992354262', '10.0', 'FORTALEZA', 'AJUDABOT')
    p.gerarPayload()
    check = []
    while True:
        try:
            horario()
            resultado = []
            cor = []
            sleep(1.4)

            # Fazendo a requisição para a API
            data_double = requests.get('https://blaze1.space/api/singleplayer-originals/originals/roulette_games/recent/1')
            resp_double = data_double.json()  # O método .json() já retorna os dados em formato de dicionário/lista

            # Iterando sobre os resultados
            for i in resp_double:
                resultado.append(i['roll'])
            
            for x in resultado:
                n = int(x)
                cor.append("V" if 1 <= n <= 7 else "P" if 8 <= n <= 14 else "B")
            
            if check != resultado and len(resultado) != 0:
                check = resultado
                # print(resultado)
                # print(cor)
                estrategia(resultado, cor)  # Chamando a função estratégia com os dados processados

        except ExceptionGroup as e:
            print(f"erro:{e}")
            pass
        
main()