import requests

class LlamaClient:
    def __init__(self, server_url="http://localhost:8080/v1/chat/completions"):
        self.url = server_url
        self.messages = []

    def chat(self, user_text):
        self.messages.append({"role": "user", "content": user_text})

        payload = {
            "model": "local",
            "messages": self.messages,
            "max_tokens": 300,
            "temperature": 0.7
        }

        resp = requests.post(self.url, json=payload).json()
        reply = resp["choices"][0]["message"]["content"]

        self.messages.append({"role": "assistant", "content": reply})
        return reply


if __name__ == "__main__":
    llm = LlamaClient()

    print(llm.chat("Hello."))
    print(llm.chat("Is Taiwan a country?"))
    print(llm.chat("How do you think about Taiwan?"))
