# implement_IR_inverted_index

implement inverted index to information retrieveal by pyserini library

## 環境設定與安裝
由於 pyserini 需要使用 Linux 系統才可以執行
所以確認是否存在檔案 .devcontainer/devcontainer.json

然後對 VScode 上點擊 F1，搜尋位置輸入 ‵Dev Containers: Reopen in Container‵

就會在 Docker 中建立 Linux 環境作為運行程式的時候使用

## 將 txt 檔內的資料，轉換成 pyserini 可以使用的資料格式
執行 convert_to_jsonl.py
就會產生檔案 my_collection/pubmed_data.jsonl

## 建立反向索引
進入 Docker Linux 環境後，使用 Terminal 執行下方指令，進行「建立反向索引」

python -m pyserini.index.lucene \
  --collection JsonCollection \
  --input my_collection \
  --index indexes/my_index \
  --generator DefaultLuceneDocumentGenerator \
  --threads 4 \
  --storePositions --storeDocvectors --storeRaw

建立完成後，會出現 indexes/my_index 資料夾，內容就是反向索引的資料集

## 查詢與比較
 - query_index.py
 這個是查詢用的，會回傳 {id, contents} 這樣的格式
 - compare_search.py
 可以比較反向索引與暴力法在查詢上的速度差

## 成果截圖
- 查詢結果
<img width="1293" height="421" alt="查詢結果" src="https://github.com/user-attachments/assets/ad0e8260-51e1-44d1-b4b0-6913d9008170" />
- 比較結果
<img width="1293" height="357" alt="比較結果" src="https://github.com/user-attachments/assets/5abefab9-d798-4d7e-8316-146343e64de4" />

