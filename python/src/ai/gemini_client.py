from dotenv import load_dotenv
import os
from google import genai


class GeminiClient:
    """
    Điểm chạm DUY NHẤT tới Google Gemini SDK trong toàn bộ dự án.
    Không module nào khác được phép import google.genai trực tiếp.
    """

    def __init__(self, model_name: str = "gemini-flash-latest"):
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise Exception("Khong tim thay GEMINI_API_KEY")

        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def ask(self, prompt: str) -> str:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        return response.text

    def list_models(self) -> list[str]:
        names = []
        for m in self.client.models.list():
            names.append(m.name)
        return names