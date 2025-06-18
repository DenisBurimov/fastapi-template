from .gpt_client import ask_gpt
from .ollama_client import ask_ollama
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s")


def ask_llm(
    prompt: str,
    model: str = "gpt",
    filepath: str | None = None,
):
    if model == "gpt":
        logger.info("Asking GPT")
        response = ask_gpt(prompt, filepath)
    else:
        logger.info("Asking Ollama %s", model)
        response = ask_ollama(prompt, model, filepath)

    return response
