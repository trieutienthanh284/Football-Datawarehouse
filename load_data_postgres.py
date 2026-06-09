import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Cập nhật đường dẫn vào thư mục EPL
csv_file = "data_epl/master_matches_dataset.csv"

if not os.path.exists(csv_file):
    print(f"Thất bại: Không tìm thấy file dữ liệu tại {csv_file}")
    exit()

df = pd.read_csv(csv_file)
engine = create_engine(DATABASE_URL)

print("Đang nạp dữ liệu và thiết lập cấu trúc bảng chuẩn trên Cloud...")
try:
    df.to_sql(
        name='fact_matches',
        con=engine,
        if_exists='replace',  # CHÚ Ý: Vẫn dùng 'replace' cho lần này để tạo lại bảng có cột league_name
        index=False,
        chunksize=100
    )
    print("THÀNH CÔNG! Bảng fact_matches trên Cloud đã được nâng cấp Schema mới.")

except Exception as e:
    print(f"Đã xảy ra lỗi trong quá trình nạp dữ liệu: {e}")