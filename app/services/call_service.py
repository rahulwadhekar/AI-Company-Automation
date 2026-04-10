# app/services/call_service.py

import logging
from app.services.knowledge_service import get_knowledge_context
from app.core.llm import llm
from app.prompts.call_prompt import CALL_PROMPT
from app.prompts.system_prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def generate_call_script(task: str, user_id: int):
    try:
        logger.info("📞 Generating call script...")

        context = get_knowledge_context(task, user_id)

        prompt = SYSTEM_PROMPT + "\n" + CALL_PROMPT.format(
            context=context,
            task=task
        )

        response = llm.complete(prompt)

        return response.text

    except Exception as e:
        logger.exception(e)
        return f"Error: {str(e)}"