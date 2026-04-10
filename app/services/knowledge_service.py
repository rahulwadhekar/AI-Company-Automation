from llama_index.core.vector_stores import MetadataFilters, MetadataFilter, FilterOperator
from app.core.vector_store import index
from app.utils.deduplicator import remove_duplicates
from app.utils.token_limiter import limit_tokens


def get_knowledge_context(query: str, user_id: int, top_k: int = 5):
    filters = MetadataFilters(
        filters=[
            MetadataFilter(
                key="user_id",
                value=str(user_id),
                operator=FilterOperator.EQ
            )
        ]
    )

    retriever = index.as_retriever(
        similarity_top_k=top_k,
        filters=filters
    )

    nodes = retriever.retrieve(query)

    chunks = [node.node.text for node in nodes if node.node.text]

    clean_chunks = remove_duplicates(chunks)

    context = "\n\n".join(clean_chunks)

    context = limit_tokens(context, max_tokens=3000)

    if not context:
        return "No relevant knowledge found."

    return context