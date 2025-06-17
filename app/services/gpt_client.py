from openai import OpenAI
from config import Settings


CFG = Settings()

client = OpenAI(api_key=CFG.OPENAI_API_KEY)


def ask_gpt(prompt: str, filepath: str | None = None):
    if filepath:
        with open(filepath, "r", encoding="utf-8") as f:
            file_content = f.read()
        prompt = f"{prompt}\n\nFile content: {file_content}"

    response = client.chat.completions.create(model="gpt-4o", messages=[{"role": "user", "content": prompt}])
    answer_choices = response.choices
    message = answer_choices[0] if answer_choices else "Failed to get a gpt answer"
    return message
