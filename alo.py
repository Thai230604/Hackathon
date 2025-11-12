import os
import base64
import json
from pdf2image import convert_from_path
from openai import OpenAI
from datetime import datetime
import io
from dotenv import load_dotenv

load_dotenv()

# === CONFIG ===
PDF_PATH = "docs/FJP Organization Chart_v1.6.pdf"  # ĐẶT FILE PDF VÀO CÙNG THƯ MỤC
OUTPUT_MD = "fjp_calendar_2025.md"
DPI = 400  # Càng cao càng rõ số nhỏ

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))  # Dùng GPT-4o vision

def pdf_to_base64_images(pdf_path, dpi=400):
    print(f"Đang chuyển {pdf_path} thành ảnh (DPI={dpi})...")
    images = convert_from_path(pdf_path, dpi=dpi)
    print(f"→ {len(images)} trang")
    return [pil_to_base64(img) for img in images]

def pil_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

def extract_full_calendar_with_vlm(images_base64):
    print("Đang dùng GPT-4o để đọc toàn bộ lịch...")
    results = []

    for idx, img_b64 in enumerate(images_base64):
        print(f"  Trang {idx+1}/{len(images_base64)}...")

        response = client.chat.completions.create(
            model="gpt-4o-2024-11-20",
            messages=[
                {
                    "role": "system",
                    "content": """
                    Bạn là chuyên gia đọc lịch công ty Nhật Bản. 
                    Trích xuất TẤT CẢ thông tin:
                    - Ngày nào là FJP Holiday (màu xanh lá)
                    - Ngày nào là National Holiday (màu cam)
                    - Ngày nào là Encouraging Annual Leave (màu xanh dương)
                    - Ghi rõ tháng, ngày, lý do nếu có
                    Trả về dạng markdown bảng hoặc danh sách rõ ràng.
                    """
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Trích xuất toàn bộ ngày nghỉ có màu từ trang này. Ghi rõ màu và ý nghĩa."},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64,{img_b64}"}
                        }
                    ]
                }
            ],
            temperature=0,
            max_tokens=1000
        )
        results.append(response.choices[0].message.content.strip())

    return "\n\n".join(results)

def save_to_markdown(content):
    header = f"""# LỊCH FPT JAPAN 2025 - ĐÃ TRÍCH XUẤT TỰ ĐỘNG  
> **File PDF**: `{PDF_PATH}`  
> **Thời gian trích xuất**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  
> **Phương pháp**: GPT-4o Vision + PDF → PNG (DPI {DPI})  
> **Không cần chạy lại** — chỉ cần đọc file này!  

---

## CHỮ KÝ MÀU
| Màu | Ý nghĩa |
|-----|--------|
| <span style="color:#008000">███ Xanh lá</span> | **FJP Holiday** - Nghỉ công ty |
| <span style="color:#FF8C00">███ Cam</span> | **National Holiday** - Nghỉ quốc gia |
| <span style="color:#00B0F0">███ Xanh dương</span> | **Encouraging Annual Leave** - Khuyến khích nghỉ phép |

---

## CHI TIẾT NGÀY NGHỈ

"""
    full_content = header + content

    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(full_content)
    
    print(f"HOÀN TẤT! File đã lưu: `{OUTPUT_MD}`")
    print(f"→ Mở bằng VSCode, Notepad++, hoặc bất kỳ app nào để đọc!")

# === CHẠY CHỈ 1 LẦN ===
if __name__ == "__main__":
    if not os.path.exists(PDF_PATH):
        print(f"Không tìm thấy file: {PDF_PATH}")
        print("Đặt file PDF vào cùng thư mục và chạy lại!")
        exit()

    images = pdf_to_base64_images(PDF_PATH, DPI)
    extracted_text = extract_full_calendar_with_vlm(images)
    save_to_markdown(extracted_text)