'''
Python script to batch rename files.
'''
import os
import random
import string

def get_random_filename_stem(length=6):
    """Generates a random numeric string of a given length."""
    return ''.join(random.choices(string.digits, k=length))

def batch_rename_image_prefix_to_random_jpg(root_folder, prefix="Image_"):
    """
    Batch renames files starting with a specific prefix in all subdirectories
    of root_folder to "random_number.jpg".

    Args:
        root_folder (str): The root directory to search for files.
        prefix (str): The prefix of filenames to rename.
    """
    renamed_count = 0
    skipped_count = 0
    error_count = 0

    if not os.path.isdir(root_folder):
        print(f"錯誤：資料夾 '{root_folder}' 不存在。")
        return

    print(f"開始在 '{root_folder}' 中重新命名檔案...")

    for subdir, _, files in os.walk(root_folder):
        print(f"\n正在處理資料夾：'{subdir}'")
        for filename in files:
            original_filepath = os.path.join(subdir, filename)
            if os.path.isfile(original_filepath) and filename.startswith(prefix):
                # Generate a new random filename (e.g., 123456.jpg)
                # Ensure the new filename doesn't already exist in the current directory
                while True:
                    random_digits = get_random_filename_stem(6) # 6-digit random number
                    new_filename = f"{random_digits}.jpg" # Force .jpg extension
                    new_filepath = os.path.join(subdir, new_filename)
                    if not os.path.exists(new_filepath):
                        break
                
                try:
                    os.rename(original_filepath, new_filepath)
                    print(f"  已重新命名：'{filename}' -> '{new_filename}'")
                    renamed_count += 1
                except OSError as e:
                    print(f"  錯誤：無法重新命名 '{filename}'：{e}")
                    error_count += 1
            elif os.path.isfile(original_filepath):
                # print(f"  跳過 (前綴不符)：'{filename}'") # Optional: for verbose logging
                skipped_count +=1 # Count files not matching the prefix

    print("\n--- 重新命名完成 ---")
    print(f"成功重新命名檔案數：{renamed_count}")
    if skipped_count > 0 :
        print(f"跳過檔案數 (前綴不符或非檔案)：{skipped_count}")
    if error_count > 0:
        print(f"發生錯誤檔案數：{error_count}")
    
    if renamed_count == 0 and error_count == 0:
        if skipped_count > 0:
            print(f"在 '{root_folder}' 中沒有找到以 '{prefix}' 開頭的檔案進行重新命名。")
        else:
            print(f"在 '{root_folder}' 中沒有找到任何檔案。")

if __name__ == '__main__':
    print("批次重新命名檔案工具")
    print("--------------------")
    print("此工具會將指定資料夾及其子資料夾中，所有以 'Image_' 開頭的檔案，")
    print("重新命名為 '隨機六位數字.jpg'。")
    print("警告：此操作無法復原，請謹慎操作，建議先備份重要檔案。")
    print("--------------------\n")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_target_folder = os.path.join(script_dir, "downloaded_google_images")

    target_folder_input = input(f"請輸入要處理的根資料夾路徑 (預設為 '{default_target_folder}'): ").strip()
    
    target_folder = default_target_folder
    if target_folder_input: # If user provided input, use it
        target_folder = target_folder_input
    
    # Validate the final target_folder path
    if not os.path.isdir(target_folder):
        print(f"錯誤：指定的資料夾 '{target_folder}' 不存在或不是一個有效的資料夾。")
        # Attempt to resolve if it was a relative path from script_dir, if input was given
        if target_folder_input:
            potential_path_from_script_dir = os.path.join(script_dir, target_folder_input)
            if os.path.isdir(potential_path_from_script_dir):
                print(f"您是指 '{potential_path_from_script_dir}' 嗎？")
                confirm_potential = input("是否使用此路徑 (y/n)? ").lower()
                if confirm_potential == 'y':
                    target_folder = potential_path_from_script_dir
                else:
                    print("操作已取消。請檢查路徑並重試。")
                    exit()
            else:
                print("請檢查路徑並重試。")
                exit()
        else: # Default path was invalid
             print("預設路徑無效。請檢查路徑並重試。")
             exit()
            
    print(f"目標資料夾設定為：'{target_folder}'")

    confirm = input(f"即將處理資料夾 '{target_folder}' 中的檔案。\n是否繼續 (y/n)？ ").lower()
    
    if confirm == 'y':
        batch_rename_image_prefix_to_random_jpg(target_folder)
    else:
        print("操作已取消。")
