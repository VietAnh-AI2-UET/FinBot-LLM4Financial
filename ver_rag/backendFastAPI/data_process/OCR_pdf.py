import time
import requests
import os
import fitz
from PIL import Image
from data_process.processing_md import preprocessing_md
path_server = '' 
url_ocr = f"{path_server}/ocr"
url_status = f"{path_server}/status"

# pdf_path = "000000015210814_Cty_me.pdf"

def clear_folder_files(folder_path):
    """
    Xóa tất cả file trong folder_path, không xóa thư mục con.
    """
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' không tồn tại.")
        return
    
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                print(f"Đã xóa file: {file_path}")
            except Exception as e:
                print(f"Lỗi khi xóa file {file_path}: {e}")
                
output_folder = "tmp_ocr_results"
def extract_img(pdf_path, out_folder):
    os.makedirs(out_folder, exist_ok=True)
    clear_folder_files(out_folder)
    doc = fitz.open(pdf_path)
    for i, page in enumerate(doc):
        pix = page.get_pixmap(dpi=100)
        img_path_png = f"{out_folder}/page_{i+1:03}.png"
        pix.save(img_path_png)

        img = Image.open(img_path_png)
        img_path_jpg = img_path_png.replace(".png", ".jpg")
        img.convert("RGB").save(img_path_jpg, "JPEG", quality=80)
        os.remove(img_path_png)
    print("✅ Đã lưu ảnh xong")

def process_pdf_file(pdf_path):
    folder_img_path = "tmp_image_pdf"
    os.makedirs(output_folder, exist_ok=True)
    clear_folder_files(output_folder)
    extract_img(pdf_path, folder_img_path)

    all_files = sorted([
        os.path.join(folder_img_path, f) 
        for f in os.listdir(folder_img_path) 
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ])
        # Gửi ảnh và lấy job_id
    files = [("files", open(f, "rb")) for f in all_files]
    res = requests.post(url_ocr, files=files, verify=False)
    for f in files:  # đóng file tránh memory leak
        f[1].close()

    if res.status_code != 202:
        print("❌ Lỗi HTTP:", res.status_code, res.text)


    job_id = res.json().get("job_id")
    if not job_id:
        print("❌ Không nhận được job_id")

    # Polling lấy kết quả
    while True:
        status_res = requests.get(f"{url_status}/{job_id}", verify=False)
        if status_res.status_code != 200:
            print("❌ Lỗi khi kiểm tra job:", status_res.text)
            break

        job_info = status_res.json()
        if job_info["status"] == "finished":
            md_contents = job_info["result"]
            for i, md_text in enumerate(md_contents, 0):
                file_path = os.path.join(output_folder, f"page_{i+1:03}.md")
                with open(file_path, "w", encoding="utf-8") as md_file:
                    md_file.write(md_text)
            print(f"✅ Lưu thành công {len(md_contents)} file .md")
            break
        elif job_info["status"] == "error":
            print("❌ OCR lỗi:", job_info["result"])
            break
        else:
            print("⏳ Đang OCR... chờ 5s")
            time.sleep(5)
    preprocessing_md(output_folder)
# process_pdf_file(pdf_path)
