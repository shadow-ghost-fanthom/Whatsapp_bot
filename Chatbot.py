import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# CHAVE API
genai.configure(api_key="AIzaSyAxPOxuc5LY5cywfCGqncixqCPkn5budXE")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    # .strip() remove qualquer espaço invisível que venha na mensagem
    pergunta = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    if not pergunta:
        return str(resp)

    try:
        # Forçamos o uso do modelo flash
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(pergunta)
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO: {e}")
        resposta_texto = "Desculpe, tive um erro na conexão com a IA."

    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)