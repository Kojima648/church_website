import os
import csv
from bs4 import BeautifulSoup

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 定义 HTML 和 CSV 目录
html_folder = os.path.join(script_dir, "TableHTML")
csv_folder = os.path.join(script_dir, "TableCSV")

# 确保 CSV 输出目录存在
os.makedirs(csv_folder, exist_ok=True)

# 遍历 TableHTML 目录中的所有 HTML 文件
for file_name in os.listdir(html_folder):
    if file_name.endswith(".html"):
        html_file = os.path.join(html_folder, file_name)
        csv_file = os.path.join(csv_folder, file_name.replace(".html", ".csv"))

        # 读取 HTML 文件
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # 查找表格
        table = soup.find("table", {"id": "calendar-table"})

        if table:
            # 提取表头
            headers = [th.get_text(strip=True) for th in table.find("thead").find_all("th")]

            # 提取数据
            data = []
            for row in table.find("tbody").find_all("tr"):
                cols = row.find_all(["th", "td"])  # 处理所有 <th> 和 <td>

                if len(cols) < len(headers):  # 确保列数匹配表头
                    continue

                # 获取前三列文本内容
                row_data = [col.get_text(strip=True) for col in cols[:3]]

                # 处理 "节日" 列：提取 <ul> 内部的 HTML，去掉外层 <td>
                festival_td = cols[3]
                ul_content = festival_td.find("ul")  # 只提取 <ul> 及其内容

                # 确保只保留 <ul> 内部的 HTML
                festival_html = str(ul_content) if ul_content else ""

                # 添加到数据列表
                data.append(row_data + [festival_html])

            # 生成 CSV 文件（**utf-8-sig 避免 Excel 乱码**）
            with open(csv_file, "w", newline="", encoding="utf-8-sig") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(headers)  # 自动写入表头
                writer.writerows(data)

            print(f"✅ 转换完成: {csv_file}")
        else:
            print(f"⚠️ 未找到表格，跳过: {html_file}")

print("🎉 所有 HTML 文件已转换为 CSV！")
