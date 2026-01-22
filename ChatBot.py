from google import genai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

# --- CONFIGURAÇÃO ---
# Sua chave de API
client = genai.Client(api_key="AIzaSyARxvFj3JulkC2o1OFQfVfehgVUig50hoQ")

# Instrução de Sistema (O "Cérebro" do Bot)
INSTRUCAO = (
    "Você é o 'DevMaster', um assistente especializado em programação para a nossa comunidade. "
    "Sua missão é tirar dúvidas de Python, JavaScript, HTML, CSS e Banco de Dados. "
    "Responda de forma técnica, mas amigável, e sempre incentive os membros a estudarem. "
    "Se alguém perguntar algo que não seja de tecnologia, tente puxar o assunto de volta para programação."
)

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    msg_recebida = request.values.get('Body', '')
    
    try:
        # Gerando a resposta com o modelo e a instrução
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            config={'system_instruction': INSTRUCAO},
            contents=msg_recebida
        )
        texto_resposta = response.text
            
    except Exception as e:
        print(f"ERRO: {e}")
        texto_resposta = "Opa, tive um erro aqui no meu compilador interno! Pode repetir?"

    # Resposta para o WhatsApp (Twilio)
    resp = MessagingResponse()
    resp.message(texto_resposta)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

