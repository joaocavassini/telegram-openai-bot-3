import requests
import time
import os

# Variáveis de ambiente (use variáveis seguras no deploy)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"

def get_updates(offset=None):
    url = TELEGRAM_API_URL + "getUpdates"
    params = {"timeout": 100, "offset": offset}
    response = requests.get(url, params=params)
    return response.json()

def send_message(chat_id, text):
    url = TELEGRAM_API_URL + "sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, data=payload)

def ask_openai(question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "Você é um assistente de inglês, especializado no curso da Rock Academy. Responda às perguntas de inglês de maneira clara e didática."},
            {"role": "user", "content": question}
        ]
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                if "message" in update:
                    chat_id = update["message"]["chat"]["id"]
                    text = update["message"].get("text")
                    if text:
                        # Comandos personalizados
                        if text.startswith("/start"):
                            response = "Olá! Sou seu assistente de inglês da Rock Academy. Tire sua dúvida sobre o curso ou inglês!"
                        elif text.startswith("/ajuda"):
                            response = "Envie suas perguntas em inglês ou sobre o curso. Estou aqui para ajudar!"
                        elif text.startswith("/dica"):
                            response = "Dica de inglês: Use 'there is' para singular e 'there are' para plural!"
                        elif text.startswith("/sobre"):
                            response = "Este bot foi criado para alunos da Rock Academy. Aqui você tira dúvidas de inglês a qualquer momento!"
                        else:
                            response = ask_openai(text)  # Pergunta ao modelo para qualquer dúvida do aluno
                        send_message(chat_id, response)
        time.sleep(1)

if __name__ == "__main__":
    main()
