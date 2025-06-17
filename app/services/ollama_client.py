import time
from ollama import Client
from config import Settings


CFG = Settings()

PROMPTS = {
    "borsch_recipe": "Будь ласка напиши мені рецепт українського борщу",
    "borsch_poem": "Будь ласка напиши мені вірша на 12 строчок українською мовою про борщ",
    "exclude_word_from_list": "Яке слово зайве в цьому списку: ['стіна', 'стеля', 'підлога', 'вікно', 'картина']",
    "java_mvc": "Could you please write a Java code for an MVC controller",
    "sql": "Could you please write a nested SQL query to find all transactions by a user",
}


ollama_client = Client()
prompt = PROMPTS["borsch_recipe"]
# prompt = PROMPTS["exclude_word_from_list"]
# prompt = PROMPTS["borsch_poem"]
# prompt = PROMPTS["java_mvc"]
# prompt = PROMPTS["sql"]

start_time = time.time()
response = ollama_client.generate(
    # model="mixtral",
    # model="mixtral:8x22b",
    model="deepseek-r1:32b",
    # model="command-a",
    # model="aya:35b",
    prompt=prompt,
    system="You are a helpful assistant that always responds in Ukrainian.",
    # system="You are a helpful IDE code assistant.",
    options={
        "temperature": 0.5,
        # "num_predict": 1024,
    },
)
print(response.get("response"))
print(f"Execution time {time.time() - start_time}")
