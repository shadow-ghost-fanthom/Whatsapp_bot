import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import google.generativeai as genai

# Configuração da API Key (Troque pela sua se gerar uma nova)
genai.configure(api_key="AIzaSyAxPOxuc5LY5cywfCGqncixqCPkn5budXE", transport='rest')

app = Flask(__name__)

# Definindo a personalidade do Especialista
instrucao_sistema = (
    "Você é um Especialista em Programação Sênior, com conhecimento profundo em todas as "
    "linguagens de programação, arquitetura de software, bancos de dados e engines de jogos "
    "(Unity, Unreal, Godot). Sua missão é ajudar o usuário com códigos eficientes, "
    "explicações didáticas e melhores práticas de desenvolvimento."
)

@app.route("/webhook", methods=['POST'])
def webhook():
    pergunta = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    
    if not pergunta:
        return str(resp)

    try:
        # Configurando o modelo com a instrução de especialista
        model = genai.GenerativeModel(
            model_name='gemini-pro',
            system_instruction=instrucao_sistema
        )
        
        response = model.generate_content(pergunta)
        resposta_texto = response.text
        
    except Exception as e:
        print(f"ERRO NO GEMINI: {e}")
        resposta_texto = "Ops, tive um problema técnico aqui. Pode tentar perguntar de novo?"

    resp.message(resposta_texto)
    return str(resp)

if __name__ == "__main__":
    # O Render usa a porta 10000 por padrão
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
