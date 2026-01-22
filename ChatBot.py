import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Use sua chave do AI Studio aqui
genai.configure(api_key="AIzaSyA8v2Ql0VsvQP9I8kxazK5Mmlx6aPm23Yk")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    
    try:
        # Mudando para o modelo 'gemini-pro' que é mais estável nessa biblioteca
        model = genai.GenerativeModel('gemini-1.5-flash')
        # OU use o antigo se o flash falhar:
        # model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(pergunta)
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO NO GEMINI: {e}")
        resposta_texto = "Oi! O DevMaster está processando muitas informações. Pode repetir?"

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
