import json
import requests
import os
from dotenv import load_dotenv

# Tải các biến môi trường trong .env vào chương trình
load_dotenv()

# Sử dụng os.getenv để lấy giá trị
API_KEY = os.getenv("FOOTBALL_API_KEY")
if not API_KEY:
    raise ValueError("FOOTBALL_API_KEY not set")

# Link lấy BXH EPL
url = "http://api.football-data.org/v4/competitions/PL/matches"

# Header để xác thực truy cập
headers = {'X-Auth-Token': API_KEY}

# Kết nối đến máy chủ
response = requests.get(url, headers=headers)
if response.status_code == 200:
    raw_data = response.json()
    with open("premier_league_matches_raw.json", "w", encoding = "utf-8") as file:
        json.dump(raw_data, file, ensure_ascii=False, indent=4)
    print('Đã lấy và lưu dữ liệu')
else:
    print(f"Có lỗi xảy ra. Mã lỗi HTTP: {response.status_code}")
    print("Chi tiết lỗi:", response.text)