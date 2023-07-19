import PyPDF2
import openai
from bardapi import Bard
import os


class PDFTools:
    def __init__(self, path: str) -> None:
        self.path = path
        self.pdfreader = PyPDF2.PdfFileReader(open(self.path, "rb"))

    def read(self) -> str:
        self.num_pages = self.pdfreader.numPages
        pageobj = self.pdfreader.getPage(self.num_pages+1)
        self.text: str = pageobj.extractText()
        return self.text


class OpenAIBot:
    def __init__(self,  api_key: str, model="gpt-3.5-turbo-0301", max_tokens=200, temperature=0.9):
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        openai.api_key = api_key

    def chat(self, user_input: str):
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system",
                    "content": "You are a resume analyser to extract his best skills."},
                {"role": "user", "content": f"{user_input}"},
            ],
            max_tokens=self.max_tokens,
            temperature=self.temperature,
        )
        return response["choices"][0]["message"]


class BardBot:
    def __init__(self,  api_key: str):
        self.api_key = api_key

    def chat(self, kwargs: dict):
        os.environ['_BARD_API_KEY'] = self.api_key
        response = Bard().get_answer(f"Find {kwargs['Professor']}'s google scholar profile from {kwargs['University']} and summarise its best work in 50 words in single line in second person")
        return response['content']


