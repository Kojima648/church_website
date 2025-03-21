import os
import re
from bs4 import BeautifulSoup

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 存放提取结果的文件夹
output_folder = os.path.join(script_dir, "TableHTML")
os.makedirs(output_folder, exist_ok=True)

# 遍历下载数据的文件夹
for year in range(2027, 2051):
    for month in range(1, 13):
        folder_name = f"{year}年{month:02d}月"
        folder_path = os.path.join(script_dir, folder_name)
        index_html_path = os.path.join(folder_path, "index.html")

        if os.path.exists(index_html_path):
            print(f"正在处理: {index_html_path}")

            # 读取 index.html 内容
            with open(index_html_path, "r", encoding="utf-8") as f:
                html_content = f.read()

            # 使用 BeautifulSoup 解析 HTML
            soup = BeautifulSoup(html_content, "html.parser")

            # 找到 <table id="calendar-table" class="table">
            table = soup.find("table", {"id": "calendar-table", "class": "table"})

            if table:
                output_file = os.path.join(output_folder, f"{year}年{month:02d}月.html")
                
                # 保存提取的表格
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(str(table))

                print(f"提取成功: {output_file}")
            else:
                print(f"未找到 <table id='calendar-table'>，跳过: {index_html_path}")
        else:
            print(f"未找到 index.html，跳过: {folder_path}")

print("所有表格提取完成！")
