import os
import re
import subprocess
import time
import shutil

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# goclone.exe 路径（与脚本同目录）
goclone_path = os.path.join(script_dir, "goclone.exe")

# 纪念日文件夹路径
memorial_folder = os.path.join(script_dir, "纪念日")
os.makedirs(memorial_folder, exist_ok=True)  # 确保目录存在

# 纪念日.ini 文件路径
ini_file = os.path.join(memorial_folder, "纪念日.ini")

# 正则匹配 `<a href="./index.php?m=saint&code=1011701"><i class="bi bi-dot"></i>圣安当院长</a>`
pattern = re.compile(r'<a href="\./index\.php\?m=saint&code=(\d+)">.*?</i>(.*?)</a>')

# 读取 纪念日.ini 文件
with open(ini_file, "r", encoding="utf-8") as file:
    lines = file.readlines()

# 处理每一行的链接
for line in lines:
    match = pattern.search(line)
    if match:
        code = match.group(1)  # 提取 code 编号
        name = match.group(2).strip()  # 提取名称并去除多余空格

        # 生成目标文件夹名（格式：圣安当院长-saint-1011701）
        folder_name = f"{name}-saint-{code}"
        folder_path = os.path.join(memorial_folder, folder_name)

        # **如果文件夹已存在，则跳过**
        if os.path.exists(folder_path):
            print(f"⏩ {folder_name} 已存在，跳过下载")
            continue

        os.makedirs(folder_path, exist_ok=True)  # 创建目录

        # 生成 URL
        url = f"https://www.wanyouzhenyuan.cn/index.php?m=saint&code={code}"
        print(f"正在下载: {url} -> 存入 {folder_path}")

        # 执行 goclone 进行下载
        try:
            subprocess.run([goclone_path, url], check=True)

            # 等待一小段时间，确保文件下载完成
            time.sleep(2)

            # 找到新下载的文件夹（goclone 默认会以域名创建目录）
            site_folder = os.path.join(script_dir, "www.wanyouzhenyuan.cn")
            if os.path.exists(site_folder):
                for item in os.listdir(site_folder):
                    item_path = os.path.join(site_folder, item)
                    shutil.move(item_path, folder_path)  # 移动文件到目标文件夹

                # 删除空目录
                os.rmdir(site_folder)

        except subprocess.CalledProcessError as e:
            print(f"下载失败: {url} - 错误: {e}")

print("🎉 所有页面下载完成！")
