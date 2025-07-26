
import pandas as pd
import matplotlib.pyplot as plt
import io

# --- Bước 1: Chuẩn bị dữ liệu ---
# Thay vì đọc từ file, chúng ta sẽ mô phỏng file bằng dữ liệu bạn đã cung cấp.
# Điều này giúp code có thể chạy ở bất cứ đâu mà không cần file CSV.

csv_data = """Country Name,Country Code,Series Name,Series Code,2017 [YR2017],2018 [YR2018],2019 [YR2019],2020 [YR2020],2021 [YR2021],2022 [YR2022],2023 [YR2023],2024 [YR2024]
Viet Nam,VNM,"Unemployment with advanced education (% of total labor force with advanced education)",SL.UEM.ADVN.ZS,4.001,2.075,2.531,4.483,3.414,2.936,2.688,..
Viet Nam,VNM,"Unemployment, youth total (% of total labor force ages 15-24) (national estimate)",SL.UEM.1524.NE.ZS,7.302,4.791,5.8,6.787,7.011,5.999,6.421,..
Viet Nam,VNM,"Unemployment, total (% of total labor force) (national estimate)",SL.UEM.TOTL.NE.ZS,1.874,1.161,1.681,2.103,2.385,1.523,1.645,..
,,,,,,,,,,,
,,,,,,,,,,,
,,,,,,,,,,,
"Data from database: World Development Indicators",,,,,,,,,,,
"Last Updated: 07/01/2025",,,,,,,,,,,
"""

# --- Bước 2: Đọc dữ liệu vào pandas DataFrame ---
# io.StringIO cho phép pandas đọc một chuỗi (string) như là một file.
# skipfooter=5: Bỏ 5 dòng thừa ở cuối.
# na_values='..': Xử lý giá trị '..' thành ô trống (NaN).
data_io = io.StringIO(csv_data)
df = pd.read_csv(data_io, skipfooter=5, na_values='..', engine='python')

# --- Bước 3: Làm sạch và chuẩn bị dữ liệu cho việc vẽ biểu đồ ---

# 3.1. Làm sạch tên các cột năm (ví dụ: '2017 [YR2017]' -> '2017')
new_columns = {col: col.split(' ')[0] for col in df.columns if '[YR' in col}
df.rename(columns=new_columns, inplace=True)

# 3.2. Chuyển đổi dữ liệu từ "dài" sang "rộng" để vẽ biểu đồ
# Đặt 'Series Name' làm chỉ mục (index)
pivoted_df = df.set_index('Series Name')

# Chọn các cột năm có dữ liệu (2017-2023)
year_columns = [str(year) for year in range(2017, 2024)]
pivoted_df = pivoted_df[year_columns]

# Chuyển vị (Transpose) để các năm là hàng, các chỉ số là cột
plot_data = pivoted_df.T

# 3.3. Đổi tên các cột để biểu đồ dễ đọc hơn
plot_data.rename(columns={
    'Unemployment with advanced education (% of total labor force with advanced education)': 'Lao động trình độ cao',
    'Unemployment, youth total (% of total labor force ages 15-24) (national estimate)': 'Thất nghiệp thanh niên (15-24)',
    'Unemployment, total (% of total labor force) (national estimate)': 'Thất nghiệp chung'
}, inplace=True)

# Đảm bảo index (các năm) là kiểu số
plot_data.index = plot_data.index.astype(int)

print("--- Dữ liệu đã sẵn sàng để vẽ biểu đồ ---")
print(plot_data)

# --- Bước 4: Trực quan hóa dữ liệu ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(14, 8))

# Vẽ biểu đồ đường với các điểm đánh dấu
plot_data.plot(kind='line', marker='o', ax=ax, linewidth=2.5)

# Tùy chỉnh biểu đồ cho chuyên nghiệp
ax.set_title('So sánh Tỷ lệ thất nghiệp tại Việt Nam (2017-2023)', fontsize=18, weight='bold', pad=20)
ax.set_xlabel('Năm', fontsize=12)
ax.set_ylabel('Tỷ lệ thất nghiệp (%)', fontsize=12)
ax.legend(title='Nhóm lao động', fontsize=11, frameon=True, shadow=True)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# Đảm bảo các nhãn trên trục x là số nguyên (các năm)
ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
plt.xticks(rotation=0)
plt.tight_layout() # Tự động căn chỉnh
plt.show()