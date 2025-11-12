import os
import asyncio
from lightrag.utils import setup_logger
# from pypdf import PdfReader
from index.ingestion import initialize_rag
from query.retrieve import run_async_query
from configs.config import WORKING_DIR, MODE
from dotenv import load_dotenv

load_dotenv()
setup_logger("log/lightrag", level="INFO")


async def main(question: str, mode: str, working_dir: str):
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
    question = "base on this file and do not search internet answer this question: ひかり電話工事（番ポ工事）結果（IN）で流通される「番ポ工事結果コード」の出力帳票と出力画面を教えてください by folowing this schema 【回答スキーマ】 1. 帳票（ちょうひょう／Report） 　・出力有無（例：出力なし／出力あり） 　・根拠（例：「流通項目仕様書」シート項番XXXXの出力情報列に〇印なし） 2. 画面（がめん／Screen） 　・画面名（例：番ポ工事結果情報画面） 　・表示内容概要（例：BB-CASTARから受信した事業者別工事結果を一覧表示、最大300番号） 　・根拠（例：「画面表示情報」列に〇印あり） 3. 補足（任意） 　・設計・運用上の備考（例：帳票出力機能は不要、表示のみで完結"
    # data_path = os.path.join(os.path.dirname(__file__), FILE_PATH)
    working_dir = WORKING_DIR
    mode = MODE
    asyncio.run(main(question=question, mode=mode, working_dir=working_dir))