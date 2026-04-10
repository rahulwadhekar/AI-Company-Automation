# app/services/agent_service.py

import logging
import traceback

from app.services.knowledge_service import get_knowledge_context
from app.core.llm import llm
from app.prompts.agent_prompt import AGENT_PROMPT
from app.prompts.system_prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def run_agent(task: str, user_id: int):
    try:
        logger.info("🤖 Running AI agent...")

        context = get_knowledge_context(task, user_id)

        prompt = SYSTEM_PROMPT + "\n" + AGENT_PROMPT.format(
            context=context,
            task=task
        )

        response = llm.complete(prompt)

        return response.text

    except Exception as e:
        logger.error(traceback.format_exc())
        return f"Error: {str(e)}"


# 🔥 Smart routing agent
def run_smart_agent(task: str, user_id: int):
    task_lower = task.lower()

    if "email" in task_lower:
        from app.services.email_service import generate_email
        return generate_email(task, user_id)

    elif "call" in task_lower or "script" in task_lower:
        from app.services.call_service import generate_call_script
        return generate_call_script(task, user_id)

    else:
        return run_agent(task, user_id)