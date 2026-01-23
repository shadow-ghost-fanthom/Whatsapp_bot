import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configuração da API Key
genai.configure(api_key="AIzaSyAxPOxuc5LY5cywfCGqncixqCPkn5budXE", transport='rest')

app = Flask(__name__)

# Personalidade de Especialista
instrucao_sistema = (
    "Você é um Especialista em Programação Sênior. Domina todas as linguagens, "
    "frameworks e engines (Unity, Unreal). Responda de forma técnica e clara."
)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    if not pergunta:
        return str(resp)

    try:
        # Usando o nome completo do modelo mais atual
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=instrucao_sistema
        )
        response = model.generate_content(pergunta)
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO NO GEMINI: {e}")
        resposta_texto = "Ops, tive um problema técnico. Pode repetir a pergunta?"

    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
