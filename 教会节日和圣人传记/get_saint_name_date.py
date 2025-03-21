import os
import csv
from bs4 import BeautifulSoup

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 纪念日文件夹（源文件夹）
memorial_folder = os.path.join(script_dir, "纪念日")

# 目标 CSV 文件
output_csv_path = os.path.join(script_dir, "纪念日配置表.csv")

# 创建 CSV 文件并写入表头
with open(output_csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # 确保所有数据都存储为字符串
    writer.writerow(["文件夹名", "圣人名称", "介绍", "纪念日"])  # 表头

    # 遍历纪念日文件夹中的所有子文件夹
    for folder_name in sorted(os.listdir(memorial_folder)):  
        folder_path = os.path.join(memorial_folder, folder_name)
        index_html_path = os.path.join(folder_path, "index.html")

        print(f"🔍 处理: {folder_name}")

        # 确保 index.html 存在
        if not os.path.exists(index_html_path):
            print(f"⚠️  {folder_name}: index.html 不存在，跳过")
            continue  

        try:
            # 读取 HTML 并忽略乱码
            with open(index_html_path, "r", encoding="utf-8", errors="ignore") as file:
                soup = BeautifulSoup(file, "html.parser")

            # **只在 `col-lg-12 article` 下面查找数据**
            article_section = soup.find("div", class_="col-lg-12 article")
            if not article_section:
                print(f"❌ {folder_name}: 未找到 `col-lg-12 article`，跳过")
                continue  

            # **提取 圣人名称**
            saint_name_tag = article_section.find("div", class_="article-title")
            saint_name = saint_name_tag.text.strip() if saint_name_tag and saint_name_tag.text.strip() else "未知"

            # **寻找 `article-subtitle`（保证只解析这个范围内的 `text-line-1` 和 `text-end`）**
            article_subtitle = article_section.find("div", class_="article-subtitle")

            description = ""
            memorial_day = "未知"

            if article_subtitle:
                # **提取 `text-line-1` 介绍**
                text_line_tag = article_subtitle.find("div", class_="text-line-1")
                if text_line_tag and text_line_tag.text.strip():
                    description = text_line_tag.text.strip()

                # **提取 `text-end` 纪念日**
                text_end_tag = article_subtitle.find("div", class_="text-end")
                if text_end_tag and text_end_tag.text.strip():
                    for icon in text_end_tag.find_all("i"):  # 去掉 `<i>` 标签
                        icon.extract()
                    memorial_day = text_end_tag.text.strip()

            # **确保 `介绍` 为空时，不填充 `text-end`**
            if not description:
                description = ""

            # **打印调试信息**
            print(f"📌 {folder_name}: 圣人名称='{saint_name}', 介绍='{description}', 纪念日='{memorial_day}'")

            # **写入 CSV**
            writer.writerow([folder_name, saint_name, description, memorial_day])

            print(f"✅ {folder_name}: 已添加到 CSV")

        except Exception as e:
            print(f"🚨 {folder_name}: 处理失败，错误: {str(e)}")

print(f"🎉 纪念日配置表已生成 -> {output_csv_path}")
