import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# API KEY
genai.configure(api_key="AIzaSyAxPOxuc5LY5cywfCGqncixqCPkn5budXE")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    if not pergunta:
        return str(resp)

    try:
        # Usando o 1.0-pro que é mais estável no Render
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(pergunta)
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO NO GEMINI: {e}")
        resposta_texto = "Ops, tive um problema aqui. Tente novamente!"

    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

