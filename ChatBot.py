import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configuração da API (Cole sua chave nova aqui)
genai.configure(api_key="AIzaSyA8v2Ql0VsvQP9I8kxazK5Mmlx6aPm23Yk")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    
    try:
        # Usando o modelo Pro que é o mais compatível com a biblioteca clássica
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        instrucao = "Você é o DevMaster, especialista em programação. Responda de forma curta e amigável."
        response = model.generate_content(f"{instrucao}\n\nUsuário: {pergunta}")
        
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO REAL: {e}")
        resposta_texto = "DevMaster em manutenção rápida. Tente em 10 segundos!"

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
