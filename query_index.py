import json
import sys
import math
from pyserini.search.lucene import LuceneSearcher
from pyserini.index.lucene import LuceneIndexReader

# 1. 指定索引資料夾路徑
index_dir = 'indexes/my_index'

# 2. 載入反向索引與索引讀取器
print("⏳ 正在載入索引庫與統計資料，請稍候...")
try:
    searcher = LuceneSearcher(index_dir)
    reader = LuceneIndexReader(index_dir) # 🌟 新增：用來讀取底層詞彙統計資訊
    total_docs = reader.stats()['documents'] # 取得總文章數 (N)
    print(f"✅ 索引載入完成！(目前庫內共有 {total_docs} 篇文章)")
except Exception as e:
    print(f"❌ 載入失敗，請確認索引路徑是否正確: {e}")
    sys.exit(1)

print("=" * 50)

while True:
    # 3. 從 Terminal 接收使用者輸入
    query = input("\n🔍 請輸入要查詢的字詞 (輸入 'q' 或 'exit' 離開): ")

    if query.lower() in ['q', 'exit']:
        print("👋 結束查詢系統，掰掰！")
        break

    if not query.strip():
        continue

    # ==========================================
    # 🌟 新增功能：計算並印出查詢詞的 IDF 值
    # ==========================================
    print(f"\n📊 詞彙 IDF 分析 (總文件數 N={total_docs}):")

    # 將查詢字串依照空格拆成單字 (處理多個詞的查詢，如 "breast cancer")
    terms = query.strip().split()
    for term in terms:
        # Pyserini 預設建立索引時會轉小寫，這裡配合轉小寫來查表
        term_lower = term.lower()

        # 取得 DF (Document Frequency: 該詞出現在幾篇文章中)
        term_counts = reader.get_term_counts(term_lower)
        df = term_counts[0] if term_counts else 0

        if df > 0:
            # 使用 Lucene BM25 預設的 IDF 公式： ln(1 + (N - DF + 0.5) / (DF + 0.5))
            idf = math.log(1 + (total_docs - df + 0.5) / (df + 0.5))
            print(f"   ➤ '{term_lower}': 出現篇數(DF) = {df}, IDF = {idf:.5f}")
        else:
            print(f"   ➤ '{term_lower}': 出現篇數(DF) = 0, IDF = 0.00000 (索引中完全沒有這個詞)")

    # 執行搜尋
    k_results = 3
    hits = searcher.search(query, k=k_results)

    print(f"\n--- 搜尋結果: '{query}' (前 {k_results} 筆) ---")

    # 4. 依照指定格式輸出結果
    for i in range(len(hits)):
        hit = hits[i]
        doc_id = hit.docid
        score = hit.score

        # 透過 searcher 提取完整文章內容
        doc = searcher.doc(doc_id)
        if doc is None:
            continue

        raw_content_string = doc.raw()

        # 解析 JSON 格式的原始內容
        try:
            doc_data = json.loads(raw_content_string)
            text_content = doc_data.get('contents', '')
        except json.JSONDecodeError:
            text_content = raw_content_string

        # 第一行：[排名] [文件ID] [總分數]
        print(f"{i + 1} {doc_id} {score:.5f}")

        # 接下來的 JSON 區塊
        print("{")
        print(f'  "id" : "{doc_id}",')

        clean_content = text_content.replace('\n', ' ').strip()
        print(f'  "contents" : " {clean_content[:70]}..."')

        print("}")

    print("-" * 50)