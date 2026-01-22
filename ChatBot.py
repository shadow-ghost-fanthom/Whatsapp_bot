import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configure sua API Key aqui
genai.configure(api_key="AIzaSyA8v2Ql0VsvQP9I8kxazK5Mmlx6aPm23Yk")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    try:
        # Usando o modelo estável para evitar o erro 404 de modelo não encontrado
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(pergunta)
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO GEMINI: {e}")
        resposta_texto = "Opa, tive um pequeno soluço técnico. Pode repetir?"

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
