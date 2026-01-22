import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configuração da API - Garanta que a chave está correta aqui
genai.configure(api_key="AIzaSyA8v2Ql0VsvQP9I8kxazK5Mmlx6aPm23Yk")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    resposta_texto = ""
    
    # Lista de nomes que o Google aceita (tentaremos um por um)
    modelos_para_testar = ['gemini-1.5-flash', 'gemini-pro', 'models/gemini-pro']
    
    for nome_modelo in modelos_para_testar:
        try:
            model = genai.GenerativeModel(nome_modelo)
            response = model.generate_content(pergunta)
            resposta_texto = response.text
            if resposta_texto: # Se conseguiu resposta, para de tentar
                break
        except Exception as e:
            print(f"Tentativa com {nome_modelo} falhou: {e}")
            continue
    
    # Se todas as tentativas falharem
    if not resposta_texto:
        resposta_texto = "O DevMaster está com o cérebro em atualização. Tente novamente em um minuto!"

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
