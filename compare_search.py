import time
import json
from pyserini.search.lucene import LuceneSearcher

# ==========================================
# 參數設定區 (請確認路徑與你實際的檔案名稱相符)
# ==========================================
query = "cancer"  # 使用你資料集裡面確實存在的詞彙
jsonl_file = 'my_collection/pubmed_data.jsonl'  # 你原本轉好的 JSONL 檔案路徑
index_dir = 'indexes/my_index'             # Pyserini 剛建立好的索引資料夾路徑

print(f"=== 搜尋關鍵字: '{query}' ===\n")

# ==========================================
# 測試一：使用反向索引搜尋 (Pyserini)
# ==========================================
print("開始執行【反向索引搜尋】...")

# 載入索引 (在實務系統中，Searcher 會一直開啟在記憶體中，因此這段載入時間通常不計入單次搜尋時間)
searcher = LuceneSearcher(index_dir)

index_start_time = time.time()
# k=1000 代表最多回傳 1000 筆相關結果
hits = searcher.search(query, k=1000)
index_end_time = time.time()

index_duration = index_end_time - index_start_time
print(f"-> 找到 {len(hits)} 筆結果")
print(f"-> 耗時: {index_duration:.6f} 秒\n")


# ==========================================
# 測試二：使用暴力搜尋法 (Linear Scan)
# ==========================================
print("開始執行【暴力搜尋法】...")

linear_start_time = time.time()
linear_results = []

# 從頭到尾逐行掃描原始 JSONL 檔案
with open(jsonl_file, 'r', encoding='utf-8') as f:
    for line in f:
        doc = json.loads(line)
        # 暴力字串比對：檢查查詢詞是否在文章內容中 (轉小寫以忽略大小寫差異)
        if query.lower() in doc['contents'].lower():
            linear_results.append(doc['id'])

linear_end_time = time.time()

linear_duration = linear_end_time - linear_start_time
print(f"-> 找到 {len(linear_results)} 筆結果")
print(f"-> 耗時: {linear_duration:.6f} 秒\n")


# ==========================================
# 結論：效能比較
# ==========================================
print("=== 效能比較結果 ===")
if index_duration > 0:
    speedup = linear_duration / index_duration
    print(f"🏆 反向索引比暴力搜尋快了約 {speedup:.2f} 倍！")
