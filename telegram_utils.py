
from telegram import Update
from telegram.ext import CallbackContext
from utils.analysis import analisar_jogos, analisar_jogo_individual
from utils.prediction import prever_resultado
from utils.betting import sugestao_aposta

def enviar_mensagem(bot, texto):
    bot.send_message(chat_id="@SINAIS_PH_CHANNEL", text=texto)

def handle_comandos(update_data, bot):
    message = update_data.get("message") or update_data.get("edited_message")
    if not message or "text" not in message:
        return

    texto = message["text"]
    chat_id = message["chat"]["id"]

    if texto.startswith("/analise"):
        if " x " in texto:
            jogo = texto.replace("/analise", "").strip()
            resposta = analisar_jogo_individual(jogo)
        else:
            resposta = "\n\n".join(analisar_jogos())
        resposta += "\n" + sugestao_aposta()
        bot.send_message(chat_id=chat_id, text=resposta)

    elif texto.startswith("/prever"):
        jogo = texto.replace("/prever", "").strip()
        resposta = prever_resultado(jogo)
        bot.send_message(chat_id=chat_id, text=resposta)
