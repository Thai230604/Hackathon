import os
import asyncio
from lightrag.utils import setup_logger
# from pypdf import PdfReader
from index.ingestion import initialize_rag, index_data
from query.retrieve import run_async_query
from configs.config import WORKING_DIR, MODE, FILE_PATH
from dotenv import load_dotenv

load_dotenv()
setup_logger("log/lightrag", level="INFO")


async def main(question: str, mode, data_path: str, working_dir: str):
    try:
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)

        # Initialize RAG instance
        rag = await initialize_rag(working_dir=working_dir)

        # Index data
        # await index_data(rag, data_path)

        # Perform hybrid search
        result = await run_async_query(rag=rag, question=question, mode=mode)
        print(result)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.finalize_storages()

if __name__ == "__main__":
    question = "who is ceo"
    data_path = os.path.join(os.path.dirname(__file__), FILE_PATH)
    working_dir = WORKING_DIR
    mode = MODE
    asyncio.run(main(question=question, mode=mode, data_path=data_path, working_dir=working_dir))