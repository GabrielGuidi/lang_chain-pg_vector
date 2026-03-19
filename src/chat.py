import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from search import search_prompt

load_dotenv()

llm_model_name = os.getenv("GOOGLE_CHAT_MODEL")
if not llm_model_name:
    raise RuntimeError("A variável de ambiente GOOGLE_CHAT_MODEL não foi definida.")

model = ChatGoogleGenerativeAI(model=llm_model_name)

def main():
    start_instruction = (
        "Você é um assistente útil que fala APENAS PT-BR. "
        "Apresente-se brevemente e convide o usuário a fazer perguntas sobre o documento PDF que você conhece. "
        "No final, avise explicitamente que o usuário deve digitar 'sair' para que o chat seja encerrado."
    )
    
    try:
        intro_response = model.invoke([HumanMessage(content=start_instruction)])
        print("Chatbot: " + intro_response.content)
    except Exception as e:
        print(f"\nErro na inicialização do chat! Mensagem: {e}")
        return

    while True:
        question = input("\nUser: ").strip()
        
        if not question:
            continue
            
        if question.lower() == "sair":
            print("\nChat encerrado.")
            break
            
        try:
            prompt_text = search_prompt(question)
            response = model.invoke(prompt_text)
            
            print(f"Chatbot: {response.content}")
            
        except Exception as e:
            print(f"\nErro ao processar a pergunta: {e}")

if __name__ == "__main__":
    main()