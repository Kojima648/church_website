import os
import shutil
from bs4 import BeautifulSoup

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 纪念日文件夹（源文件夹）
memorial_folder = os.path.join(script_dir, "纪念日")

# 目标文件夹（用于存放复制的图片）
output_folder = os.path.join(script_dir, "整理后的图片")
os.makedirs(output_folder, exist_ok=True)  # 确保目标目录存在

# 遍历纪念日文件夹中的所有子文件夹
for folder_name in sorted(os.listdir(memorial_folder)):  
    folder_path = os.path.join(memorial_folder, folder_name)
    index_html_path = os.path.join(folder_path, "index.html")
    images_folder = os.path.join(folder_path, "imgs")  # 确定图片所在的文件夹

    # 处理当前目录
    print(f"🔍 处理: {folder_name}")

    # 确保子目录存在
    if not os.path.exists(folder_path):
        print(f"❌  {folder_name}: 目录不存在，跳过")
        continue  

    # 确保 index.html 存在
    if not os.path.exists(index_html_path):
        print(f"⚠️  {folder_name}: index.html 不存在，跳过")
        continue  

    try:
        with open(index_html_path, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # 找到 class="article-content"
        article_content = soup.find(class_="article-content")

        if not article_content:
            print(f"⚠️  {folder_name}: 未找到 article-content，跳过")
            continue  

        # 查找所有 <img> 标签
        images = article_content.find_all("img")
        if not images:
            print(f"⚠️  {folder_name}: 该文章没有图片，跳过")
            continue  

        # 处理图片
        image_count = 0
        for img in images:
            img_src = img.get("src")
            if not img_src:
                continue  

            # **修正关键点：去掉末尾 `/`**
            img_src = img_src.rstrip("/")  

            # **拼接完整的图片路径**
            img_path = os.path.join(folder_path, img_src)

            # **如果路径无效，尝试从 imgs 目录查找**
            if not os.path.exists(img_path):
                img_path = os.path.join(images_folder, os.path.basename(img_src))

            # **如果仍然找不到，打印调试信息**
            if not os.path.exists(img_path):
                print(f"❌  {folder_name}: 图片 {img_src} 不存在，跳过")
                continue  

            # 生成新文件名
            image_count += 1
            new_filename = f"{folder_name}.jpg"
            new_file_path = os.path.join(output_folder, new_filename)

            # 复制文件
            shutil.copy2(img_path, new_file_path)
            print(f"✅ {folder_name}: 复制 {img_src} -> {new_filename}")

    except Exception as e:
        print(f"🚨 {folder_name}: 处理失败，错误: {str(e)}")

print("🎉 图片整理完成！所有图片已保存到 '整理后的图片' 文件夹")
