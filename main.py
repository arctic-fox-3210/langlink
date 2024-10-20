import file_process
from LLM import gemini


if __name__ == "__main__":
    LLM = gemini.gemini_ai()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        response = LLM.chat(user_input)
        print(f"Gemini: {response}")
    LLM.get_history()