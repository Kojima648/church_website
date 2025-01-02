import os
import shutil
import subprocess

# 配置参数
def main():
    # version = input("请输入圣经版本 (例如: sigao): ")
    version = "sigao"
    template = input("请输入模板编号: ")
    # chapter = input("请输入起始章节 (例如: 0): ")
    chapter = 0

    base_url = f"https://www.wanyouzhenyuan.cn/index.php?m=bible&version={version}&template={template}&chapter="
    goclone_path = "D:\\Downloads\\goclone_v1.2.1_windows_x86_64\\goclone.exe"  # goclone.exe 的路径
    temp_dir = "D:\\Downloads\\goclone_v1.2.1_windows_x86_64\\python_downloader\\www.wanyouzhenyuan.cn"  # 正确的默认下载位置
    output_dir = f"D:\\Downloads\\goclone_v1.2.1_windows_x86_64\\cloned_bible\\version={version}&template={template}"  # 保存克隆结果的目录

    # 确定章节范围
    start_chapter = int(chapter)
    end_chapter = int(input("请输入结束章节: "))

    # 创建保存目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 批量克隆脚本
    for chapter in range(start_chapter, end_chapter + 1):
        url = f"{base_url}{chapter}"
        chapter_dir = os.path.join(output_dir, f"chapter_{chapter}")

        # 确保章节目录存在
        if not os.path.exists(chapter_dir):
            os.makedirs(chapter_dir)

        # 调用 goclone
        command = [goclone_path, url]
        try:
            print(f"Cloning chapter {chapter} from {url}...")
            result = subprocess.run(command, capture_output=True, text=True)

            if result.returncode == 0:
                print(f"Successfully cloned chapter {chapter}. Checking files in {temp_dir}...")
                # 检查临时目录是否有文件
                if os.path.exists(temp_dir):
                    files_found = os.listdir(temp_dir)
                    if files_found:
                        print(f"Found files in {temp_dir}: {files_found}")
                        for item in files_found:
                            item_path = os.path.join(temp_dir, item)
                            target_path = os.path.join(chapter_dir, item)

                            # 移动文件或目录到目标章节目录
                            shutil.move(item_path, target_path)
                            print(f"Moved {item} to {chapter_dir}")
                        print(f"All files for chapter {chapter} have been moved to {chapter_dir}.")
                    else:
                        print(f"No files found in {temp_dir} for chapter {chapter}.")
                else:
                    print(f"Temporary directory {temp_dir} does not exist.")
            else:
                print(f"Error cloning chapter {chapter}: {result.stderr}")
        except Exception as e:
            print(f"Exception occurred while cloning chapter {chapter}: {e}")

    print("All chapters processed.")

if __name__ == "__main__":
    main()