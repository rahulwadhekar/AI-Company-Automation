# app/core/vector_store.py

import os
import logging
from urllib.parse import urlparse

from llama_index.vector_stores.postgres import PGVectorStore
from llama_index.core import StorageContext, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex

# 🔥 Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

logger.info("=" * 60)
logger.info("🚀 INITIALIZING VECTOR STORE")
logger.info("=" * 60)

# ---------------- ENV ----------------
DATABASE_URL = os.getenv("DATABASE_URL")

logger.info(f"🔗 DATABASE_URL: {DATABASE_URL}")

if not DATABASE_URL:
    logger.error("❌ DATABASE_URL is None!")
    raise ValueError("DATABASE_URL is missing")
else:
    logger.info("✅ DATABASE_URL loaded")

# ---------------- PARSE DATABASE URL ----------------
logger.info("🔍 Parsing DATABASE_URL...")

try:
    parsed = urlparse(DATABASE_URL)

    DB_HOST = parsed.hostname
    DB_PORT = parsed.port
    DB_USER = parsed.username
    DB_PASSWORD = parsed.password
    DB_NAME = parsed.path.lstrip("/")

    logger.info("✅ DATABASE PARSED SUCCESSFULLY")
    logger.info(f"Host: {DB_HOST}")
    logger.info(f"Port: {DB_PORT}")
    logger.info(f"User: {DB_USER}")
    logger.info(f"Database: {DB_NAME}")

    if not DB_PORT:
        raise ValueError("❌ Port is None → DATABASE_URL parsing failed")

except Exception as e:
    logger.error("❌ DATABASE PARSING FAILED")
    logger.exception(e)
    raise

# ---------------- EMBEDDING MODEL ----------------
logger.info("🧠 Loading embedding model...")

try:
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="BAAI/bge-small-en"
    )
    logger.info("✅ Embedding model loaded")
    logger.info("📏 Expected embedding dimension: 384")

except Exception as e:
    logger.error("❌ Embedding model load failed")
    logger.exception(e)
    raise

# ---------------- VECTOR STORE ----------------
logger.info("🗄️ Creating PGVectorStore...")

try:
    vector_store = PGVectorStore.from_params(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        table_name="documents",
        embed_dim=384,
        perform_setup=True,
        use_jsonb=True,
        hybrid_search=False
    )

    logger.info("✅ PGVectorStore created successfully")

except Exception as e:
    logger.error("❌ Failed to create PGVectorStore")
    logger.exception(e)
    raise

# ---------------- STORAGE CONTEXT ----------------
logger.info("📦 Creating StorageContext...")

try:
    storage_context = StorageContext.from_defaults(
        vector_store=vector_store
    )
    logger.info("✅ StorageContext created")

except Exception as e:
    logger.error("❌ StorageContext creation failed")
    logger.exception(e)
    raise

# ---------------- FINAL DEBUG ----------------
logger.info("🔍 FINAL DEBUG INFO")

logger.info(f"Vector Store Object: {vector_store}")
logger.info(f"Storage Context: {storage_context}")

try:
    logger.info(f"📂 Table Name: {vector_store.table_name}")
    logger.info(f"📏 Embedding Dim: {vector_store.embed_dim}")
except Exception as e:
    logger.warning(f"⚠️ Could not access attributes: {e}")

logger.info("=" * 60)
logger.info("✅ VECTOR STORE INITIALIZED SUCCESSFULLY")
logger.info("=" * 60)


index = VectorStoreIndex.from_vector_store(
    vector_store,
    storage_context=storage_context
)