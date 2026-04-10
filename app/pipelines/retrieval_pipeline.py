from app.services.knowledge_service import get_knowledge_context

def build_context(query, user_id):
    context = get_knowledge_context(query, user_id)

    return f"""
Use ONLY the below knowledge:

{context}

Instructions:
- Do not repeat
- Be structured
- Be concise
"""