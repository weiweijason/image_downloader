'''
Python script to download images from Google Images and name them automatically.

Disclaimer:
- This script is for educational purposes and demonstrates web scraping basics.
- Scraping Google Search results might be against their Terms of Service.
- Google's HTML structure can change, breaking the script.
- Frequent requests might lead to IP blocking.
- For reliable access, consider using official APIs like Google Custom Search API.
'''
import requests
from bs4 import BeautifulSoup
import os
import time
import re
import random # 匯入 random 模組

def sanitize_filename(name):
    """ Sanitize a string to be used as a filename. """
    name = re.sub(r'[<>:"/\\|?*]', '', name) # Remove invalid characters
    name = name.replace(' ', '_') # Replace spaces with underscores
    return name[:200] # Limit filename length

def download_google_images(query, num_images=10, output_folder='images'):
    """
    Downloads images from Google Images based on a query.

    Args:
        query (str): The search query for images.
        num_images (int): The number of images to attempt to download.
        output_folder (str): The folder where images will be saved.
    """
    sanitized_query_for_folder = sanitize_filename(query)
    specific_output_folder = os.path.join(output_folder, sanitized_query_for_folder)

    if not os.path.exists(specific_output_folder):
        os.makedirs(specific_output_folder)
        print(f"已建立資料夾：{specific_output_folder}")

    # Google Images search URL. This might change.
    # Using a User-Agent to mimic a browser.
    search_url = f"https://www.google.com/search?q={query}&tbm=isch"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"
    }

    print(f"正在搜尋 '{query}' 的圖片...")
    try:
        response = requests.get(search_url, headers=headers, timeout=20)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"錯誤：無法取得搜尋結果頁面 - {e}")
        print("這可能是因為網路問題，或是 Google 暫時阻擋了請求。")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    # Finding image elements. This is highly dependent on Google's current HTML structure
    # and is the most likely part to break.
    # Google uses JavaScript to load many images, so simple parsing of initial HTML might not get all results.
    # This selector targets script tags containing image data, which is a common pattern.
    image_urls = []
    # Google often embeds image data in script tags as JSON-like structures.
    # The regex tries to find URLs within these script tags.
    # This is a common but fragile way to get image URLs.
    for script_tag in soup.find_all("script"):
        if script_tag.string:
            # This regex is an attempt to find URLs within script tags.
            # It looks for common image file extensions.
            # It's not perfect and might need adjustments.
            found_urls = re.findall(r'"(https?://[^"]+\.(?:jpg|jpeg|png|gif|bmp|webp))"', script_tag.string)
            image_urls.extend(found_urls)

    # Deduplicate URLs while preserving order (for Python 3.7+)
    image_urls = list(dict.fromkeys(image_urls))

    if not image_urls:
        print("找不到圖片 URL。Google 的 HTML 結構可能已變更，或者圖片是動態載入的。")
        print("這個腳本可能需要更新 HTML 解析邏輯。")
        print("提示：檢查 Google 圖片搜尋結果頁面的原始碼，找出圖片 URL 的儲存方式。")
        return

    downloaded_count = 0
    for i, img_url in enumerate(image_urls):
        if downloaded_count >= num_images:
            break

        try:
            print(f"正在嘗試下載圖片 {downloaded_count + 1}/{num_images} 從：{img_url[:100]}...") # Print truncated URL
            img_response = requests.get(img_url, headers=headers, timeout=15, stream=True)
            img_response.raise_for_status()

            # Determine image extension
            content_type = img_response.headers.get('content-type')
            extension = '.jpg' # Default extension
            if content_type:
                if 'jpeg' in content_type:
                    extension = '.jpg'
                elif 'png' in content_type:
                    extension = '.png'
                elif 'gif' in content_type:
                    extension = '.gif'
                elif 'webp' in content_type:
                    extension = '.webp'
                elif 'bmp' in content_type:
                    extension = '.bmp'

            # Create filename: random_number.extension
            random_number = random.randint(100000, 999999) # 產生一個六位數的隨機數字
            filename = os.path.join(specific_output_folder, f"{random_number}{extension}")

            # Save the image
            with open(filename, 'wb') as f:
                for chunk in img_response.iter_content(8192):
                    f.write(chunk)
            
            print(f"已下載並儲存為：{filename}")
            downloaded_count += 1

            # Brief pause to be polite to the server
            time.sleep(0.5)

        except requests.exceptions.MissingSchema:
            print(f"無效的 URL (缺少協定)：{img_url[:100]}")
        except requests.exceptions.RequestException as e:
            print(f"無法下載圖片 {img_url[:100]}: {e}")
        except Exception as e:
            print(f"處理圖片 {img_url[:100]} 時發生未知錯誤: {e}")

    if downloaded_count == 0:
        print("\n最終沒有成功下載任何圖片。")
        print("可能原因：")
        print("1. Google 的 HTML 結構已變更，導致無法正確解析圖片 URL。")
        print("2. 您的請求被 Google 偵測為自動化行為並被阻擋。")
        print("3. 找到的 URL 無法直接存取或不是有效的圖片。")
        print("建議：考慮使用 Google Custom Search API 以獲得更可靠的結果，或手動檢查 Google 圖片頁面原始碼以更新解析邏輯。")
    else:
        print(f"\n總共下載了 {downloaded_count} 張圖片到 '{specific_output_folder}' 資料夾。")

if __name__ == '__main__':
    print("Google 圖片下載腳本")
    print("--------------------")
    print("重要提示：")
    print("1. 此腳本嘗試從 Google 圖片搜尋結果中抓取圖片。Google 的頁面結構可能會變更，導致此腳本失效。")
    print("2. 大量或頻繁的請求可能導致您的 IP 被 Google 短暫或永久封鎖。")
    print("3. 請確保您的使用行為符合 Google 的服務條款。")
    print("4. 為了更穩定和合規地存取 Google 圖片，建議研究並使用 Google Custom Search API。")
    print("5. 此腳本找到的圖片 URL 可能包含縮圖或非直接連結，下載品質不一。")
    print("--------------------\n")

    search_query = input("請輸入要搜尋的圖片關鍵字：")
    
    while True:
        try:
            num_to_download_str = input("請輸入要下載的圖片數量 (預設為 5)：")
            if not num_to_download_str:
                num_to_download = 5
                break
            num_to_download = int(num_to_download_str)
            if num_to_download > 0:
                break
            else:
                print("請輸入一個正整數。")
        except ValueError:
            print("無效的輸入，請輸入一個數字。")

    output_dir = "downloaded_google_images"

    confirm = input(f"即將搜尋 '{search_query}' 並嘗試下載 {num_to_download} 張圖片到 '{os.path.join(output_dir, sanitize_filename(search_query))}' 資料夾。\n是否繼續 (y/n)？ ").lower()
    
    if confirm == 'y':
        download_google_images(search_query, num_to_download, output_dir)
    else:
        print("操作已取消。")
