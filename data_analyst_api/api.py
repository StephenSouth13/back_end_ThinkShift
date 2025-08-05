import csv

file_path = "data/78a298f9-5116-4f7c-b7da-98eb12034756_Data.csv"

try:
   
    with open(file_path, mode='r', newline='', encoding='utf-8') as file:
      
        csv_reader = csv.reader(file)
  
 
        header = next(csv_reader)
        print(f"Tiêu đề các cột: {header}")

   
        print("\nNội dung các dòng dữ liệu:")
        for row in csv_reader:
            # Mỗi 'row' là một list các chuỗi (string)
            print(row)

except FileNotFoundError:
    print(f"Lỗi: Không tìm thấy file tại đường dẫn '{file_path}'")
except Exception as e:
    print(f"Đã xảy ra lỗi: {e}")