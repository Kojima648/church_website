import json
import csv

# 输入/输出路径
json_path = r"D:\Downloads\纪念日文章内容.json"
csv_path = r"D:\Downloads\纪念日文章内容.csv"

# 加载 JSON 文件
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# 写入 CSV
with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)
    writer.writerow(["folder_name", "title", "content"])  # 表头

    for item in data:
        folder = item.get("folder_name", "")
        title = item.get("title", "")
        content = item.get("content", "").replace("\n", "").replace("\r", "")
        writer.writerow([folder, title, content])

print("✅ JSON 转 CSV 完成，已保存为:", csv_path)
