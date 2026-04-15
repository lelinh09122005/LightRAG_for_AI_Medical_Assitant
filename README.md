# LightRAG for AI Medical Assistant 🏥🚀

Dự án xây dựng Trợ lý Y tế ảo thông minh, ứng dụng kỹ thuật Retrieval-Augmented Generation (RAG) để hỗ trợ tra cứu và cung cấp thông tin y tế một cách nhanh chóng, chính xác. 

Dự án này được tùy biến và phát triển dựa trên kiến trúc mạnh mẽ của [LightRAG](https://github.com/HKUDS/LightRAG).

## 🌟 Điểm nổi bật của dự án

* **Tối ưu hóa cho lĩnh vực Y tế:** File `Prompt.py` cốt lõi đã được viết lại và tinh chỉnh để mô hình AI có khả năng trích xuất thực thể y khoa (như triệu chứng, tên thuốc, bệnh lý) và suy luận dựa trên ngữ cảnh lâm sàng cơ bản.
* **Tốc độ truy xuất cao:** Tận dụng cơ chế lập chỉ mục dựa trên đồ thị (Graph-based Text Indexing) của LightRAG gốc để tìm kiếm thông tin nhanh chóng.
* **Dễ dàng mở rộng:** Bộ khung được thiết kế gọn nhẹ, sẵn sàng tích hợp với các bộ dữ liệu y tế lớn hơn trong tương lai.

## 🛠️ Hướng dẫn cài đặt

Dưới đây là các bước để cài đặt và chạy thử dự án trên môi trường Linux/Ubuntu:

**1. Clone dự án về máy:**
```bash
git clone [https://github.com/lelinh09122005/LightRAG_for_AI_Medical_Assitant.git](https://github.com/lelinh09122005/LightRAG_for_AI_Medical_Assitant.git)
cd LightRAG_for_AI_Medical_Assitant



# Chạy file khởi tạo trợ lý y tế
python run_chatbot.py



### Một số lưu ý nhỏ cho bạn:
* Ở phần **Hướng dẫn sử dụng**, mình đang để lệnh mẫu là `python main.py`. Nếu file chạy chính của bạn tên khác (ví dụ `app.py` hay `test.py`), bạn nhớ sửa lại cho đúng nhé.
* Sau khi dán nội dung này vào và lưu lại, bạn chỉ cần mở terminal lên và gõ lần lượt 3 lệnh: `git add README.md`, `git commit -m "Viet lại file README cho du an y te"`, và `git push` như mình đã hướng dẫn ở trên là GitHub của bạn sẽ cập nhật giao diện mới cực kỳ đẹp mắt!