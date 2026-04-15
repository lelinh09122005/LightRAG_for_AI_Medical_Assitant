import os
import asyncio
from lightrag import LightRAG, QueryParam
from lightrag.llm.ollama import ollama_model_complete, ollama_embed
from lightrag.utils import EmbeddingFunc

# Đảm bảo timeout đủ dài cho các câu trả lời phức tạp
os.environ["LIGHTRAG_LLM_WORKER_TIMEOUT"] = "600"

WORKING_DIR = "./medical_graph_db"

print("⚙️ Đang tải Database Y khoa và khởi động Llama 3.2...")

# Khởi tạo LightRAG (BẮT BUỘC phải giữ nguyên cấu hình model và embedding như lúc tạo DB)
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

async def chat_loop():
    # Load storage vào RAM
    await rag.initialize_storages()
    
    print("\n" + "="*50)
    print("🏥 CHATBOT Y KHOA (LIGHTRAG + OLLAMA) ĐÃ SẴN SÀNG!")
    print("💡 Mẹo: Gõ 'thoat' hoặc 'quit' để kết thúc trò chuyện.")
    print("="*50 + "\n")

    while True:
        user_input = input("🧑 Bạn: ")
        
        if user_input.lower() in ['thoat', 'quit', 'exit']:
            print("👋 Hẹn gặp lại!")
            break
            
        if not user_input.strip():
            continue

        print("🤖 AI đang suy nghĩ (Tìm kiếm trong Đồ thị)...")
        try:
            # Sử dụng mode='hybrid' để kết hợp tìm kiếm cả chi tiết (local) và tổng quan (global)
            answer = await rag.aquery(user_input, param=QueryParam(mode="hybrid"))
            print(f"\n🩺 Bác sĩ AI:\n{answer}\n")
            print("-" * 50)
        except Exception as e:
            print(f"\n❌ Có lỗi xảy ra trong lúc truy vấn: {e}\n")

if __name__ == "__main__":
    # Đảm bảo tắt các cảnh báo log không cần thiết khi chat
    import logging
    logging.getLogger().setLevel(logging.ERROR)
    
    asyncio.run(chat_loop())