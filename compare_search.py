import time
import json
import sys
from pyserini.search.lucene import LuceneSearcher

# ==========================================
# 參數設定區
# ==========================================
jsonl_file = 'my_collection/pubmed_data.jsonl'  # 原始 JSONL 檔案路徑
index_dir = 'indexes/my_index'             # Pyserini 索引資料夾路徑

# ==========================================
# 系統初始化 (載入反向索引)
# ==========================================
print("⏳ 正在啟動效能比較系統並載入索引庫，請稍候...")
try:
    # 載入索引 (只在程式啟動時執行一次，不計入單次搜尋時間)
    searcher = LuceneSearcher(index_dir)
    print("✅ 索引載入完成！")
except Exception as e:
    print(f"❌ 載入失敗，請確認索引路徑是否正確: {e}")
    sys.exit(1)

print("=" * 50)

# ==========================================
# 互動式查詢迴圈
# ==========================================
while True:
    # 讓使用者輸入要比較的字詞
    query = input("\n🔍 請輸入要比較搜尋速度的字詞 (輸入 'q' 或 'exit' 離開): ")

    if query.lower() in ['q', 'exit']:
        print("👋 結束效能比較系統，掰掰！")
        break

    if not query.strip():
        continue

    print(f"\n=== 🚀 開始對決：搜尋關鍵字 '{query}' ===")

    # ------------------------------------------
    # 測試一：使用反向索引搜尋 (Pyserini)
    # ------------------------------------------
    print("【1. 反向索引搜尋】執行中...")

    index_start_time = time.time()
    # k=1000 代表最多回傳 1000 筆相關結果
    hits = searcher.search(query, k=1000)
    index_end_time = time.time()

    index_duration = index_end_time - index_start_time
    print(f" -> 找到 {len(hits)} 筆結果")
    print(f" -> 耗時: {index_duration:.6f} 秒\n")

    # ------------------------------------------
    # 測試二：使用暴力搜尋法 (Linear Scan)
    # ------------------------------------------
    print("【2. 暴力搜尋法】執行中 (掃描整份 JSONL)...")

    linear_start_time = time.time()
    linear_results = []

    try:
        # 從頭到尾逐行掃描原始 JSONL 檔案
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                doc = json.loads(line)
                # 暴力字串比對：檢查查詢詞是否在文章內容中 (轉小寫以忽略大小寫差異)
                if query.lower() in doc['contents'].lower():
                    linear_results.append(doc['id'])
    except FileNotFoundError:
        print(f"❌ 找不到原始資料檔: {jsonl_file}，無法執行暴力搜尋。")
        continue

    linear_end_time = time.time()

    linear_duration = linear_end_time - linear_start_time
    print(f" -> 找到 {len(linear_results)} 筆結果")
    print(f" -> 耗時: {linear_duration:.6f} 秒\n")

    # ------------------------------------------
    # 結論：效能比較
    # ------------------------------------------
    print("=== 📊 效能比較結果 ===")
    if index_duration > 0:
        speedup = linear_duration / index_duration
        print(f"🏆 反向索引比暴力搜尋快了約 {speedup:,.2f} 倍！")
    else:
        # 避免除以零的情況 (當反向索引快到 Python 抓不到時間差)
        print("🏆 反向索引速度極快，測量時間趨近於 0 秒！")

    print("-" * 50)
