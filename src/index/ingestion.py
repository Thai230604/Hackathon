# ingestion.py
import os
import asyncio
from pypdf import PdfReader
from lightrag import LightRAG
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger

# Cấu hình logger
setup_logger("lightrag", level="INFO")

async def initialize_rag(working_dir: str):
    """Khởi tạo LightRAG và pipeline"""
    rag = LightRAG(
        working_dir=working_dir,
        embedding_func=openai_embed,
        llm_model_func=gpt_4o_mini_complete,
    )
    await rag.initialize_storages()
    await initialize_pipeline_status()
    return rag

async def index_data(rag: LightRAG, file_path: str) -> None:
    """
    Index a text file into LightRAG, tagging chunks with its filename.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    # stream chunks into vector store and graph
    await rag.ainsert(input=text, file_paths=[file_path])

