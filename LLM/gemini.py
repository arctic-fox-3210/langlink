import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

genai.configure(api_key='AIzaSyBDRyKIvpsXKYVyc1DlXv7OQK3zSDNoNTQ')

class gemini_ai:
    def __init__(self, prompt: str = "使用繁體中文進行回覆",
                 temperature: float = 1,
                 top_p: float = 0.95,
                 top_k: float = 40,
                 max_output_tokens: int = 8192,
                 response_mime_type: str = "text/plain"
                 ):
        
        self.generation_config = {
            "temperature": temperature,
            "top_p": top_p,
            "top_k": top_k,
            "max_output_tokens": max_output_tokens,
            "response_mime_type": response_mime_type,
        }

        self.model = genai.GenerativeModel(
            model_name='gemini-1.5-pro-002',
            generation_config=self.generation_config,
            system_instruction=prompt
        )

        self.history = []

        self.chat_session = self.model.start_chat(
            history=self.history
        )

    def chat(self, text: str):
        try:
            response = self.chat_session.send_message(text)
            self.history.append(
                {
                    'role':'user',
                    'parts':[
                        text
                    ],
                }                
            )
            self.history.append(
                {
                    'role':'model',
                    'parts':[
                        response.text
                    ]
                }
            )
            return response.text
        except ResourceExhausted as e:
            print(f"在調用 gemini 出現錯誤: {e}")
    
    def get_history(self):
        for history in self.history:
            print(history['parts'][0])