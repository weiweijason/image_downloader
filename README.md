# 圖片下載與批次重新命名工具

此專案包含兩個 Python 腳本，用於從 Google 圖片下載圖片，並對下載的圖片或其他指定資料夾中的圖片進行批次重新命名。

## 腳本說明

### 1. Google 圖片下載器 (`google_image_downloader.py`)

此腳本允許使用者輸入關鍵字，從 Google 圖片搜尋結果中下載指定數量的圖片。

**功能：**

*   根據使用者提供的關鍵字搜尋圖片。
*   允許使用者指定要下載的圖片數量。
*   下載的圖片會儲存在以搜尋關鍵字命名的子資料夾中（位於 `downloaded_google_images` 資料夾下）。
*   自動處理資料夾的建立。
*   嘗試從網頁中解析多種常見圖片格式 (jpg, png, gif, webp, bmp) 的 URL。
*   下載的圖片會以隨機數字命名，以避免檔名衝突並保留原始副檔名。

**如何執行：**

1.  開啟終端機或命令提示字元。
2.  導覽至腳本所在的目錄 (`c:\Users\User\OneDrive - weiweihsu\code\`)。
3.  執行命令： `python google_image_downloader.py`
4.  依照提示輸入搜尋關鍵字和要下載的圖片數量。

**依賴套件：**

*   `requests`
*   `beautifulsoup4`

如果尚未安裝，請使用 pip 安裝：
```bash
pip install requests beautifulsoup4
```

**重要注意事項：**

*   此腳本僅供教育目的，展示網頁爬蟲的基本原理。
*   爬取 Google 搜尋結果可能違反其服務條款。
*   Google 的 HTML 結構可能會變更，導致腳本失效。
*   頻繁的請求可能導致 IP 被封鎖。
*   為了更穩定和合規地存取 Google 圖片，建議研究並使用 Google Custom Search API。
*   腳本找到的圖片 URL 可能包含縮圖或非直接連結，下載品質不一。

### 2. 批次重新命名檔案 (`batch_rename_files.py`)

此腳本用於批次重新命名指定資料夾及其子資料夾中，所有以特定前綴（預設為 `Image_`）開頭的檔案。重新命名後的檔案會變成 `隨機六位數字.jpg` 的格式。

**功能：**

*   遞迴處理指定根資料夾下的所有子資料夾。
*   尋找檔名以特定前綴開頭的檔案。
*   將符合條件的檔案重新命名為六位隨機數字加上 `.jpg` 副檔名 (例如 `123456.jpg`)。
*   確保新的隨機檔名在該資料夾中是唯一的。
*   提供執行前的確認提示。

**如何執行：**

1.  開啟終端機或命令提示字元。
2.  導覽至腳本所在的目錄 (`c:\Users\User\OneDrive - weiweihsu\code\`)。
3.  執行命令： `python batch_rename_files.py`
4.  依照提示輸入要處理的根資料夾路徑（預設為 `downloaded_google_images`）。

**依賴套件：**

*   Python 標準庫 (`os`, `random`, `string`)，無需額外安裝。

**重要注意事項：**

*   **警告：此操作無法復原。** 在執行腳本之前，強烈建議您先**備份重要檔案**。
*   腳本會強制將重新命名後的檔案副檔名設為 `.jpg`，即使原始檔案是其他圖片格式（如 `.png`, `.gif`）。

## 資料夾結構

*   `google_image_downloader.py`: Google 圖片下載腳本。
*   `batch_rename_files.py`: 批次重新命名腳本。
*   `downloaded_google_images/`: `google_image_downloader.py` 預設儲存下載圖片的資料夾。
    *   `<搜尋關鍵字>/`: 每個關鍵字下載的圖片會存放在此處的子資料夾。

## 環境需求

*   Python 3.x

## 建議使用流程

1.  執行 `google_image_downloader.py` 下載您需要的圖片。圖片將儲存在 `downloaded_google_images/<搜尋關鍵字>/` 資料夾中，並以隨機數字命名。
2.  如果您有其他來源的圖片，且檔名以 `Image_` 開頭，您可以將它們整理到一個資料夾中。
3.  執行 `batch_rename_files.py`，並將目標資料夾指向包含這些 `Image_` 開頭檔案的資料夾（或 `downloaded_google_images` 資料夾，如果下載的圖片檔名需要被此腳本的規則覆蓋）。
    *   **請注意**：`google_image_downloader.py` 目前下載的檔案已經是隨機數字命名。如果您希望對這些由 `google_image_downloader.py` 下載的檔案再次使用 `batch_rename_files.py` 進行重新命名（例如，如果它們因某些原因變成了 `Image_` 開頭），請確保您了解其操作後果。

