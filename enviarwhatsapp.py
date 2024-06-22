import pywhatkit
import datetime



def enviar_whatsapp(evento, numero_destino):
    # Pega a hora atual e ajusta para enviar a mensagem um minuto depois
    agora = datetime.datetime.now()
    hora = agora.hour
    minuto = agora.minute + 1

    # Prepara a mensagem
    mensagem = f"Olá, este é um alerta de evento: {evento}!"

    # Envia a mensagem via WhatsApp
    pywhatkit.sendwhatmsg(numero_destino, mensagem, hora, minuto)

    print("Mensagem programada com sucesso!")

# Exemplo de chamada da função
enviar_whatsapp("Reunião às 15h", "+5582988152221")
