# ingestion.py
import os
import asyncio
from pypdf import PdfReader
from lightrag import LightRAG
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger
import json
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


def process_json_for_rag(json_data):
    """
    Chuyển đổi JSON thành định dạng text phù hợp cho RAG
    """
    if isinstance(json_data, dict):
        text_parts = []
        for key, value in json_data.items():
            if isinstance(value, (dict, list)):
                text_parts.append(f"{key}: {process_json_for_rag(value)}")
            else:
                text_parts.append(f"{key}: {value}")
        return "\n".join(text_parts)
    
    elif isinstance(json_data, list):
        return "\n".join([str(process_json_for_rag(item)) for item in json_data])
    
    else:
        return str(json_data)

# async def index_data(rag: LightRAG, file_path: str) -> None:
#     """
#     Index a text file into LightRAG, tagging chunks with its filename.
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Data file not found: {file_path}")

#     # with open(file_path, 'r', encoding='utf-8') as f:
#     #     text = f.read()
    # reader = PdfReader(file_path)
    # text = "\n".join([page.extract_text() for page in reader.pages])

#     # with open(file_path, 'r') as f:
#     #     json_data = json.load(f)
#     # text = process_json_for_rag(json_data)

#     # stream chunks into vector store and graph
#     await rag.ainsert(input=text, file_paths=[file_path])

# def process_json_for_rag(json_data):
#     """
#     Chuyển đổi JSON thành định dạng text phù hợp cho RAG
#     """
#     if isinstance(json_data, dict):
#         text_parts = []
#         for key, value in json_data.items():
#             if isinstance(value, (dict, list)):
#                 text_parts.append(f"{key}: {process_json_for_rag(value)}")
#             else:
#                 text_parts.append(f"{key}: {value}")
#         return "\n".join(text_parts)
    
#     elif isinstance(json_data, list):
#         return "\n".join([str(process_json_for_rag(item)) for item in json_data])
    
#     else:
#         return str(json_data)

# async def index_data(rag: LightRAG, file_path: str) -> None:
#     """
#     Index a JSON file into LightRAG, tagging chunks with its filename.
#     """
#     if not os.path.exists(file_path):
#         raise FileNotFoundError(f"Data file not found: {file_path}")

#     try:
#         # Thử các encoding khác nhau
#         encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1258']
        
#         for encoding in encodings:
#             try:
#                 with open(file_path, 'r', encoding=encoding) as f:
#                     json_data = json.load(f)
#                 print(f"Successfully read file with encoding: {encoding}")
#                 break
#             except UnicodeDecodeError:
#                 continue
#         else:
#             # Nếu tất cả encoding đều fail, thử đọc binary
#             with open(file_path, 'rb') as f:
#                 content = f.read()
#                 # Thử detect encoding
#                 import chardet
#                 detected = chardet.detect(content)
#                 encoding = detected.get('encoding', 'utf-8')
#                 json_data = json.loads(content.decode(encoding))
        
#         text = process_json_for_rag(json_data)
        
#         # stream chunks into vector store and graph
#         await rag.ainsert(input=text, file_paths=[file_path])
        
#     except Exception as e:
#         print(f"Error processing file {file_path}: {str(e)}")
#         raise

