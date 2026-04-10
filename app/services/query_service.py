import logging
import traceback

from llama_index.core.vector_stores import (
    MetadataFilters,
    MetadataFilter,
    FilterOperator
)

# 🔥 USE CENTRALIZED OBJECTS
from app.core.vector_store import index
from app.core.llm import llm

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


# ================= MAIN QUERY FUNCTION =================
def query_knowledge(query: str, user_id: int):
    try:
        logger.info("\n" + "=" * 60)
        logger.info("🚀 NEW QUERY REQUEST STARTED")
        logger.info("=" * 60)

        # ---------------- INPUT DEBUG ----------------
        logger.info(f"🔍 Query: {query}")
        logger.info(f"👤 User ID: {user_id}")
        logger.info(f"🔤 Query Length: {len(query)}")

        # ---------------- FILTER ----------------
        logger.info("🧾 Building metadata filters...")

        filters = MetadataFilters(
            filters=[
                MetadataFilter(
                    key="user_id",
                    value=str(user_id),
                    operator=FilterOperator.EQ
                )
            ]
        )

        logger.info(f"✅ Filters created: {filters}")

        # ---------------- QUERY ENGINE ----------------
        logger.info("⚙️ Creating query engine...")

        query_engine = index.as_query_engine(
            llm=llm,
            filters=filters,
            similarity_top_k=4,  # 🔥 optimized
            response_mode="tree_summarize"
        )

        logger.info("✅ Query engine created")

        # ---------------- EXECUTE QUERY ----------------
        logger.info("🔎 Executing query...")

        response = query_engine.query(query)

        logger.info("✅ Query executed successfully")

        # ---------------- EMPTY RESPONSE CHECK ----------------
        if not response or not str(response).strip():
            logger.warning("⚠️ No relevant response found")
            return "No relevant information found."

        # ---------------- SOURCE NODES DEBUG ----------------
        try:
            if hasattr(response, "source_nodes"):
                logger.info(f"📚 Retrieved {len(response.source_nodes)} source nodes")

                # 🔥 limit logs
                for i, node in enumerate(response.source_nodes[:3]):
                    logger.info(f"\n--- 🔹 NODE {i} ---")
                    logger.info(f"Score: {node.score}")

                    preview = node.node.text[:150] if node.node.text else "No text"
                    logger.info(f"Preview: {preview}")

                    logger.info(f"Metadata: {node.node.metadata}")

        except Exception:
            logger.warning("⚠️ Could not read source nodes")

        # ---------------- FINAL RESPONSE ----------------
        final_response = str(response).strip()

        logger.info("\n✅ FINAL RESPONSE:")
        logger.info(final_response)

        logger.info("=" * 60)
        logger.info("🏁 QUERY COMPLETED")
        logger.info("=" * 60)

        return final_response

    except Exception as e:
        logger.error("\n❌ QUERY FAILED")
        logger.error(f"Error: {str(e)}")

        # 🔥 FULL TRACEBACK
        logger.error(traceback.format_exc())

        return "Something went wrong while processing your query."