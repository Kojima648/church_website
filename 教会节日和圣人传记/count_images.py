import os
from bs4 import BeautifulSoup

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 纪念日文件夹路径
memorial_folder = os.path.join(script_dir, "纪念日")

# 结果文件
output_file = os.path.join(script_dir, "image_report.txt")

# 统计变量
zero_count = 0  # 0张图片的文件夹数
one_count = 0   # 1张图片的文件夹数
more_than_one_count = 0  # >1张图片的文件夹数
more_than_one_folders = []  # 记录 >1 张图片的文件夹名称

# 打开结果文件用于写入
with open(output_file, "w", encoding="utf-8") as report:
    report.write("📌 文章中图片数量统计：\n\n")

    # 遍历纪念日文件夹中的所有子文件夹
    for folder_name in sorted(os.listdir(memorial_folder)):  # 确保按字母顺序遍历
        folder_path = os.path.join(memorial_folder, folder_name)
        index_html_path = os.path.join(folder_path, "index.html")

        # 检查 index.html 是否存在
        if not os.path.exists(index_html_path):
            report.write(f"{folder_name}: ❌ index.html 文件不存在\n")
            print(f"⚠️  {folder_name}: index.html 不存在")
            continue  # 跳过此文件夹

        try:
            with open(index_html_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

            # 找到 class="article-content"
            article_content = soup.find(class_="article-content")

            if article_content:
                # 查找 <img> 标签
                images = article_content.find_all("img")
                image_count = len(images)
            else:
                image_count = 0  # 没有找到 article-content，则默认图片数为 0

        except Exception as e:
            report.write(f"{folder_name}: ❌ 读取失败（错误: {str(e)}）\n")
            print(f"🚨  {folder_name}: 读取 index.html 失败，错误: {str(e)}")
            continue  # 继续下一个文件夹

        # 统计不同类别的文件夹数量
        if image_count == 0:
            zero_count += 1
        elif image_count == 1:
            one_count += 1
        else:
            more_than_one_count += 1
            more_than_one_folders.append(folder_name)

        # 记录到文件
        report.write(f"{folder_name}: {image_count} 张图片\n")
        print(f"📌 {folder_name}: {image_count} 张图片")

    # 追加统计结果到文件末尾
    report.write("\n📊 **图片数量统计**\n")
    report.write(f"- 0 张图片的文件夹数: {zero_count} 个\n")
    report.write(f"- 1 张图片的文件夹数: {one_count} 个\n")
    report.write(f"- >1 张图片的文件夹数: {more_than_one_count} 个\n")

    # 追加大于1张图片的文件夹名称
    if more_than_one_folders:
        report.write("\n📌 **大于1张图片的文件夹**（共 {} 个）:\n".format(more_than_one_count))
        for folder in more_than_one_folders:
            report.write(f"- {folder}\n")

print("✅ 统计完成，结果已保存到 image_report.txt")
