import time
from ollama import Client
from config import Settings
import logging


CFG = Settings()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


def ask_ollama(
    prompt: str,
    model: str = "gemma",
    filepath: str | None = None,
):
    PROMPTS = {
        "borsch_recipe": "Будь ласка напиши мені рецепт українського борщу",
        "borsch_poem": "Будь ласка напиши мені вірша на 12 строчок українською мовою про борщ",
        "exclude_word_from_list": "Яке слово зайве в цьому списку: ['стіна', 'стеля', 'підлога', 'вікно', 'картина']",
        "java_mvc": "Could you please write a Java code for an MVC controller",
        "sql": "Could you please write a nested SQL query to find all transactions by a user",
    }

    MODELS = {
        "gemma": "gemma3:27b",
        "mixtral": "mixtral:8x22b",
        "deepseek": "deepseek-r1:32b",
        "aya": "aya:35b",
        "command-a": "command-a",
    }

    ollama_client = Client()
    prompt = PROMPTS["borsch_recipe"]
    model = MODELS[model]

    start_time = time.time()
    try:
        response = ollama_client.generate(
            model=model,
            prompt=prompt,
            system="You are a helpful assistant that always responds in Ukrainian.",
            options={
                "temperature": 0.5,
                # "num_predict": 1024,
            },
        )
        execution_time = time.time() - start_time
        answer = response.get("response", "")
        if answer:
            logger.info("Ask Ollama execution time: %s", execution_time)
        else:
            logger.error("Ollama failed to respond in %s", execution_time)
        return answer
    except Exception as e:
        logger.error("Ollama failed to respond %s", e)
        return str(e)
