import os
import asyncio
import logging
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

# 1. CẤU HÌNH LOGGING
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="graph_build_progress.log"
)

os.environ["LIGHTRAG_LLM_WORKER_TIMEOUT"] = "1200"

WORKING_DIR = "./medical_graph_db"
if not os.path.exists(WORKING_DIR):
    os.mkdir(WORKING_DIR)

print("⚙️ Cấu hình LightRAG (Llama 3.2 3B + mxbai-embed-large)...")

rag = LightRAG(
    working_dir=WORKING_DIR,
    llm_model_func=ollama_model_complete,
    llm_model_name="llama3.2", 
    embedding_func=EmbeddingFunc(
        embedding_dim=1024,
        max_token_size=8192,
        func=lambda texts: ollama_embed(texts, embed_model="mxbai-embed-large")
    )
)

async def main():
    await rag.initialize_storages()

    # 2. ĐỌC VÀ TÁCH DỮ LIỆU
    file_path = "medical_full_data_english_cleaned.txt"
    if not os.path.exists(file_path):
        print(f"❌ Không tìm thấy file {file_path}")
        return

    print(f"⏳ Đang đọc và phân tách dữ liệu từ {file_path}...")
    
    medical_docs = []
    with open(file_path, "r", encoding="utf-8") as f:
        # Tách file theo từ khóa "Medical Document - Topic:" 
        # Đây là cách tách an toàn nhất dựa trên cấu trúc file của bạn
        content = f.read()
        raw_docs = content.split("Medical Document - Topic:")
        
        for doc in raw_docs:
            if doc.strip():
                # Thêm lại từ khóa đã bị split mất vào đầu mỗi đoạn
                medical_docs.append("Medical Document - Topic: " + doc.strip())

    # KIỂM TRA SỐ LƯỢNG SAU KHI TÁCH
    num_docs = len(medical_docs)
    print(f"📊 Đã tách thành công: {num_docs} tài liệu riêng biệt.")
    
    if num_docs <= 1:
        print("⚠️ CẢNH BÁO: Hệ thống vẫn chỉ nhận diện được 1 tài liệu. Kiểm tra lại định dạng file text!")
        return

    print("🧠 Bắt đầu nạp dữ liệu vào Đồ thị (Batch Processing)...")
    try:
        # Nạp mảng list này vào ainsert
        await rag.ainsert(medical_docs)
        print("\n✅ HOÀN TẤT!")
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")

if __name__ == "__main__":
    asyncio.run(main())