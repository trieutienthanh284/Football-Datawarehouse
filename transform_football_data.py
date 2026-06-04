import json
import pandas as pd
import yaml

# 1. Đọc cấu hình Nguồn cũ
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

source_config = config['source_football_data_org']
raw_filename = source_config['output_file']
# Tạm thời xuất ra file csv có hậu tố để phân biệt
clean_filename = "football_data_clean.csv"

# 2. Đọc JSON cũ
with open(raw_filename, "r", encoding="utf-8") as file:
    raw_data = json.load(file)

matches = raw_data.get("matches", [])
cleaned_matches = []

# 3. Logic bóc tách (Đặc trưng của football-data.org)
for match in matches:
    referee_list = match.get("referees", [])
    main_referee = referee_list[0].get("name") if len(referee_list) > 0 else None

    match_info = {
        "match_id": match.get("id"),
        "match_date": match.get("utcDate"),
        "home_team": match.get("homeTeam", {}).get("shortName"),
        "away_team": match.get("awayTeam", {}).get("shortName"),
        "home_score": match.get("score", {}).get("fullTime", {}).get("home"),
        "away_score": match.get("score", {}).get("fullTime", {}).get("away"),
        "referee": main_referee,
        "data_source": "football-data.org" # Gắn nhãn để biết dữ liệu từ đâu
    }
    cleaned_matches.append(match_info)

df = pd.DataFrame(cleaned_matches)
df['match_date'] = pd.to_datetime(df['match_date'])
df.to_csv(clean_filename, index=False, encoding="utf-8-sig")
print(f"Đã xử lý xong Nguồn 1. Lưu tại: {clean_filename}")