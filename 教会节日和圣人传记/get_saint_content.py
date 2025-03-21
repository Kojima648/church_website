import os
import csv
from bs4 import BeautifulSoup

# WordPress 上传目录的相对路径
WP_UPLOADS_PATH = "/wp-content/uploads/2025/03/"

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 纪念日文件夹（源文件夹）
memorial_folder = os.path.join(script_dir, "纪念日")

# 目标 CSV 文件（用于存储文章内容）
output_csv_path = os.path.join(script_dir, "纪念日文章内容.csv")

# 创建 CSV 文件并写入表头
with open(output_csv_path, "w", newline="", encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)  # 确保所有数据都存储为字符串
    writer.writerow(["文件夹名", "圣人名称", "文章内容"])  # 表头

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

            # **获取 `article-content`（文章内容）**
            article_content_tag = article_section.find("div", class_="article-content")
            if not article_content_tag:
                print(f"⚠️  {folder_name}: `article-content` 为空，跳过")
                continue  
            
            # **处理图片路径**
            image_tags = article_content_tag.find_all("img")
            for img in image_tags:
                # 直接替换为 WordPress 相对路径 + 文件夹名字.png
                new_image_name = WP_UPLOADS_PATH + folder_name + ".png"
                img["src"] = new_image_name

            # **去除段落前的空格**
            for tag in article_content_tag.find_all(["p", "div", "span", "li"]):  # 清理常见的文本标签
                if tag.string:
                    tag.string = tag.string.lstrip()  # 去除前导空格

            # **转换文章 HTML**
            article_html = str(article_content_tag)

            # **打印调试信息**
            print(f"📌 {folder_name}: 圣人名称='{saint_name}', 文章内容已处理")

            # **写入 CSV**
            writer.writerow([folder_name, saint_name, article_html])

            print(f"✅ {folder_name}: 已添加到 CSV")

        except Exception as e:
            print(f"🚨 {folder_name}: 处理失败，错误: {str(e)}")

print(f"🎉 纪念日文章内容 CSV 生成完毕 -> {output_csv_path}")
