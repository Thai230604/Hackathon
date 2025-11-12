#data.py
import os
import asyncio
from pypdf import PdfReader
from lightrag import LightRAG
from lightrag.llm.openai import openai_embed, gpt_4o_mini_complete
from lightrag.kg.shared_storage import initialize_pipeline_status
from lightrag.utils import setup_logger
import json

async def index_data(rag: 'LightRAG', folder_path: str) -> None:
    if not os.path.isdir(folder_path):
        raise NotADirectoryError(f"Input path is not a valid directory: {folder_path}")
   
    for filename in os.listdir(folder_path):
        # Tạo đường dẫn đầy đủ đến tệp tin
        file_path = os.path.join(folder_path, filename)
       
        # Chỉ xử lý các tệp tin (bỏ qua các thư mục con)
        if os.path.isfile(file_path) and file_path.endswith('.txt'): # Có thể thêm điều kiện lọc file khác nếu cần
           
            # 1. Đọc nội dung file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")
                continue # Bỏ qua nếu có lỗi đọc file
 
            # 2. Stream chunks vào vector store và graph (sử dụng await)
            print(f"Indexing file: {file_path}")
            # Truyền đường dẫn đầy đủ của file làm metadata
            await rag.ainsert(input=text, file_paths=[file_path])
       
        # Có thể thêm else: để bỏ qua hoặc in cảnh báo cho các thư mục con
 
    print("Indexing process completed.")
 
 