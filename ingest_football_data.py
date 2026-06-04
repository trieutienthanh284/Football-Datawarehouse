import json
import requests
import os
import yaml
from dotenv import load_dotenv

# 1. Đọc cấu hình nguồn cũ
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

source_config = config['source_football_data_org']

# 2. Tải khóa bí mật cũ từ .env
load_dotenv()
API_KEY = os.getenv("FOOTBALL_API_KEY")
if not API_KEY:
    raise ValueError("Chưa tìm thấy FOOTBALL_API_KEY trong file .env!")

# 3. Lắp ráp URL và Tham số (Thêm querystring ở đây)
url = f"{source_config['base_url']}/{source_config['league_code']}/{source_config['endpoint']}"

# Tạo gói tham số để ép server trả về đúng mùa giải
querystring = {"season": source_config['season']}

raw_filename = source_config['output_file']
headers = {'X-Auth-Token': API_KEY}

print(f"Đang kết nối [Nguồn 1: football-data.org] để kéo dữ liệu mùa {source_config['season']}...")

# 4. Gửi yêu cầu (Nhớ truyền thêm params=querystring)
response = requests.get(url, headers=headers, params=querystring)

if response.status_code == 200:
    raw_data = response.json()
    with open(raw_filename, "w", encoding="utf-8") as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=4)
    print(f"Hoàn tất Nguồn 1! Đã lưu vào file: {raw_filename}")
else:
    print(f"Lỗi Nguồn 1 - HTTP: {response.status_code} | Chi tiết: {response.text}")