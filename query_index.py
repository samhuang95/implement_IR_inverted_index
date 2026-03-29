import json
from pyserini.search.lucene import LuceneSearcher

# 1. 指定索引資料夾路徑
index_dir = 'indexes/my_index'

# 2. 載入反向索引
searcher = LuceneSearcher(index_dir)

# 3. 設定查詢關鍵字與回傳數量
query = "cancer" # 你可以換成你想測試的字
k_results = 3

# 執行搜尋
hits = searcher.search(query, k=k_results)

# 4. 依照指定格式輸出結果
for i in range(len(hits)):
    hit = hits[i]
    doc_id = hit.docid
    score = hit.score

    # ==========================================
    # 🌟 關鍵修改：透過 searcher 提取完整文章內容
    # ==========================================
    doc = searcher.doc(doc_id)
    raw_content_string = doc.raw() # 取得當時存入的 JSONL 字串

    # 解析 JSON 格式的原始內容
    try:
        doc_data = json.loads(raw_content_string)
        text_content = doc_data.get('contents', '')
    except json.JSONDecodeError:
        text_content = raw_content_string

    # 第一行：[排名] [文件ID] [分數(取到小數點後5位)]
    print(f"{i + 1} {doc_id} {score:.5f}")

    # 接下來的 JSON 區塊
    print("{")
    print(f'  "id" : "{doc_id}",')

    # 清理內文中可能自帶的換行符號，並依照圖片格式補上一個空白
    clean_content = text_content.replace('\n', ' ').strip()

    # (如果不想印出幾千字的完整內文，可以像截圖一樣把文字截斷，例如加上 [:70])
    print(f'  "contents" : " {clean_content[:70]}"')

    print("}")