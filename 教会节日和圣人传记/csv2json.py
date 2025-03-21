# import csv
# import json
# import os

# # 获取当前目录
# script_dir = os.path.dirname(os.path.abspath(__file__))

# # CSV 文件路径
# csv_file_path = os.path.join(script_dir, "纪念日文章内容.csv")
# json_file_path = os.path.join(script_dir, "纪念日文章内容.json")

# # 读取 CSV 并转换为 JSON
# data_list = []
# with open(csv_file_path, "r", encoding="utf-8-sig") as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         data_list.append({
#             "folder_name": row["文件夹名"],
#             "title": row["圣人名称"],
#             "content": row["文章内容"]
#         })

# # 写入 JSON 文件
# with open(json_file_path, "w", encoding="utf-8") as jsonfile:
#     json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)

# print(f"✅ JSON 数据已生成: {json_file_path}")



import csv
import json
import os

# 获取当前目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# CSV 文件路径
csv_file_path = os.path.join(script_dir, "纪念日配置表.csv")
json_file_path = os.path.join(script_dir, "纪念日配置表.json")

# 读取 CSV 并转换为 JSON
data_list = []
with open(csv_file_path, "r", encoding="utf-8-sig") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data_list.append({
            "folder_name": row["文件夹名"],
            "title": row["圣人名称"],
            "description": row["介绍"] if row["介绍"] else "",  # 介绍可能为空
            "memorial_day": row["纪念日"] if row["纪念日"] else "未知"  # 纪念日为空时设为 "未知"
        })

# 写入 JSON 文件
with open(json_file_path, "w", encoding="utf-8") as jsonfile:
    json.dump(data_list, jsonfile, ensure_ascii=False, indent=4)

print(f"✅ JSON 数据已生成: {json_file_path}")
