from google import genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

# --- CONFIGURAÇÃO ---
# No Render, ele usa a biblioteca nova, então o erro 404 some
client = genai.Client(api_key="AIzaSyARxvFj3JulkC2o1OFQfVfehgVUig50hoQ")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    msg_recebida = request.values.get('Body', '')
    
    try:
        # Usamos o modelo que sua chave listou como disponível
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=msg_recebida
        )
        texto_resposta = response.text
            
    except Exception as e:
        print(f"ERRO: {e}")
        texto_resposta = "Tive um probleminha aqui, pode repetir?"

    resp = MessagingResponse()
    resp.message(texto_resposta)
    return str(resp)

if __name__ == "__main__":
    # O Render define a porta sozinho, por isso usamos esse comando
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)