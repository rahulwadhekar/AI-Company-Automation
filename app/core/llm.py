import os
import logging
from llama_index.llms.gemini import Gemini

logger = logging.getLogger(__name__)

try:
    llm = Gemini(
        model="models/gemini-3.1-flash-lite-preview",
        api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    )

    logger.info("✅ LLM initialized")

except Exception as e:
    logger.error("❌ LLM init failed")
    logger.exception(e)
    raise