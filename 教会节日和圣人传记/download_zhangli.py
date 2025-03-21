import os
import subprocess
import shutil
import time

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# goclone.exe 路径（与脚本同目录）
goclone_path = os.path.join(script_dir, "goclone.exe")

# 生成 2027 年 1 月 到 2050 年 12 月的 URL
base_url = "https://www.wanyouzhenyuan.cn/index.php?m=calendar&date={}-{:02d}"

for year in range(2027, 2051):
    for month in range(1, 13):
        url = base_url.format(year, month)
        folder_name = f"{year}年{month:02d}月"  # 目标文件夹
        save_path = os.path.join(script_dir, folder_name)

        # 确保文件夹存在
        os.makedirs(save_path, exist_ok=True)

        print(f"正在下载: {url}")

        # 执行 goclone.exe 进行下载
        try:
            subprocess.run([goclone_path, url], check=True)
            
            # 等待一小段时间，确保文件下载完成
            time.sleep(2)

            # 找到新下载的文件夹（goclone 默认会以域名创建目录）
            site_folder = os.path.join(script_dir, "www.wanyouzhenyuan.cn")
            if os.path.exists(site_folder):
                # 移动下载的文件到目标文件夹
                for item in os.listdir(site_folder):
                    shutil.move(os.path.join(site_folder, item), save_path)

                # 删除空目录
                os.rmdir(site_folder)

        except subprocess.CalledProcessError as e:
            print(f"下载失败: {url} - 错误: {e}")

print("所有数据下载完成！")
