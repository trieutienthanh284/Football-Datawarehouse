import json
import pandas as pd
import yaml

# 1. Đọc cấu hình Nguồn mới
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

source_config = config['source_api_football']
raw_filename = source_config['output_file']
clean_filename = "api_football_clean.csv"

# 2. Đọc JSON mới
with open(raw_filename, "r", encoding="utf-8") as file:
    raw_data = json.load(file)

# Chú ý: API-Football cất dữ liệu trong mảng "response"
matches = raw_data.get("response", [])
cleaned_matches = []

# 3. Logic bóc tách (Đặc trưng của API-Football)
for match in matches:
    fixture = match.get("fixture", {})
    teams = match.get("teams", {})
    goals = match.get("goals", {})
    score = match.get("score", {})

    match_info = {
        "match_id": fixture.get("id"),
        "match_date": fixture.get("date"),
        # Chú ý đường dẫn khác hoàn toàn nguồn cũ
        "home_team": teams.get("home", {}).get("name"),
        "away_team": teams.get("away", {}).get("name"),
        "home_score": goals.get("home"),
        "away_score": goals.get("away"),
        "referee": fixture.get("referee"),
        "data_source": "api-football" # Gắn nhãn
    }
    cleaned_matches.append(match_info)

df = pd.DataFrame(cleaned_matches)
df['match_date'] = pd.to_datetime(df['match_date'])
df.to_csv(clean_filename, index=False, encoding="utf-8-sig")
print(f"Đã xử lý xong Nguồn 2. Lưu tại: {clean_filename}")