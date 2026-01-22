import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from google import genai

# Configuração da API
client = genai.Client(api_key="AIzaSyARxvFj3JulkC2o1OFQfVfehgVUig50hoQ")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    
    try:
        # Instrução direta de quem o bot deve ser
        instrucao = "Você é o DevMaster, especialista em programação. Responda de forma amigável e técnica."
        
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"{instrucao}\n\nPergunta do usuário: {pergunta}"
        )
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO: {e}")
        resposta_texto = "Erro na conexão com o cérebro da IA. Verifique os logs."

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
