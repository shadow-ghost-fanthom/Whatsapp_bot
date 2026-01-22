import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configuração da API - Use a sua chave do AI Studio
genai.configure(api_key="AIzaSyA8v2Ql0VsvQP9I8kxazK5Mmlx6aPm23Yk")

app = Flask(__name__)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '')
    
    try:
        # Trocamos o nome do modelo para 'gemini-pro' que é o mais universal
        # Se não funcionar, ele tenta o flash automaticamente
        model = genai.GenerativeModel('gemini-pro')
        
        instrucao = "Você é o DevMaster, um assistente de programação gente boa."
        response = model.generate_content(f"{instrucao}\n\nUsuário: {pergunta}")
        
        resposta_texto = response.text
    except Exception as e:
        print(f"ERRO REAL: {e}")
        # Segunda tentativa com o nome alternativo se o primeiro falhar
        try:
            model = genai.GenerativeModel('gemini-1.5-flash-latest')
            response = model.generate_content(pergunta)
            resposta_texto = response.text
        except:
            resposta_texto = "Quase lá! O Google está atualizando o modelo. Tenta de novo em 5 segundos?"

    resp = MessagingResponse()
    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
