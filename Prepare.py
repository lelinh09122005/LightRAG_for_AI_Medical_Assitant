from datasets import load_dataset
import os
import re # Thêm thư viện Regex để xử lý chuỗi

def clean_text(text):
    """Hàm dọn dẹp văn bản: Xóa URL và các ký tự thừa."""
    # Xóa các đường link bắt đầu bằng http:// hoặc https://
    text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
    # Xóa các đường link bắt đầu bằng www.
    text = re.sub(r'www\.[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+', '', text)
    # Xóa các khoảng trắng thừa do việc xóa link để lại
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def fetch_and_prepare_hf_data():
    print("⏳ Fetching the full dataset from HuggingFace...")
    # Tải toàn bộ dataset
    dataset = load_dataset("medalpaca/medical_meadow_wikidoc", split="train")
    
    print(f"✅ Download complete! Total records: {len(dataset)}")
    dataset = dataset.select(range(1000))
    documents = []
    print("⏳ Converting and cleaning data...")
    
    for item in dataset:
        # SỬA LỖI 1: Lấy đúng cột 'input' làm Topic thay vì 'instruction'
        topic = item.get('input', '').strip()
        details = item.get('output', '').strip()
        
        # Nếu cột input trống, thử lấy từ instruction phòng hờ, nhưng bỏ câu lệnh thừa
        if not topic:
             instr = item.get('instruction', '')
             if "Answer this question truthfully" not in instr:
                 topic = instr.strip()
             else:
                 topic = "General Medical Condition" # Gán tên mặc định nếu không có tên bệnh
        
        if topic and details:
            # SỬA LỖI 2: Dọn sạch link rác trong phần details
            clean_details = clean_text(details)
            
            # Bỏ qua những bản ghi sau khi xóa link thì không còn nội dung gì
            if len(clean_details) > 10: 
                doc_text = f"Medical Document - Topic: {topic}. Clinical details and treatment protocol: {clean_details}."
                documents.append(doc_text)
            
    # Gộp tất cả thành một chuỗi văn bản lớn
    full_text = "\n\n".join(documents)
    
    # Lưu ra file
    output_file = "medical_full_data_english_cleaned.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_text)
        
    print(f"✅ Successfully saved clean text file at: {output_file}")
    return full_text

if __name__ == "__main__":
    prepared_text = fetch_and_prepare_hf_data()