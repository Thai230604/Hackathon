from data.data import index_data
from index.ingestion import initialize_rag
from configs.config import WORKING_DIR, FOLDER_PATH
import os
import asyncio
async def main(data_path: str, working_dir: str):
    try:
        if not os.path.exists(working_dir):
            os.mkdir(working_dir)

        # Initialize RAG instance
        rag = await initialize_rag(working_dir=working_dir)
        await index_data(rag, data_path)
  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if rag:
            await rag.finalize_storages()

if __name__ == "__main__":
    data_path = os.path.join(os.path.dirname(__file__), FOLDER_PATH)
    working_dir = WORKING_DIR
    asyncio.run(main(data_path=data_path, working_dir=working_dir))

