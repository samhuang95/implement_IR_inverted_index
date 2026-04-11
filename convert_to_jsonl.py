import json
import os

# ==========================================
# 0. 基本設定
# ==========================================
output_dir = 'my_collection'
os.makedirs(output_dir, exist_ok=True) # 確保輸出資料夾存在

# 資料集 1：PubMed 設定
pubmed_input = 'Pubmed 220 Train 2022-01-21.txt'
pubmed_output = os.path.join(output_dir, 'pubmed_data.jsonl')

# 資料集 2：Wiki 設定
wiki_input = 'wiki_article_list_2023_tra.json'
wiki_output = os.path.join(output_dir, 'wiki_data.jsonl')


# ==========================================
# 1. 處理 PubMed TXT 資料集
# ==========================================
if os.path.exists(pubmed_input):
    print("⏳ 開始處理 PubMed 資料...")
    current_id = None
    current_contents = []

    with open(pubmed_input, 'r', encoding='utf-8') as f_in, \
         open(pubmed_output, 'w', encoding='utf-8') as f_out:

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            if line.startswith('###'):
                # 寫入前一筆文獻
                if current_id is not None:
                    doc = {"id": current_id, "contents": " ".join(current_contents)}
                    f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

                # 抓取新 ID
                current_id = line[3:]
                current_contents = []
            else:
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    current_contents.append(parts[1])
                else:
                    parts = line.split(' ', 1)
                    if len(parts) == 2:
                        current_contents.append(parts[1])
                    else:
                        current_contents.append(line)

        # 處理最後一筆文獻
        if current_id is not None:
            doc = {"id": current_id, "contents": " ".join(current_contents)}
            f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

    print(f"✅ PubMed 轉換完成！檔案已儲存至: {pubmed_output}")
else:
    print(f"⚠️ 找不到檔案 {pubmed_input}，跳過 PubMed 處理。")


# ==========================================
# 2. 處理 Wiki JSON 陣列資料集
# ==========================================
if os.path.exists(wiki_input):
    print("\n⏳ 開始處理 Wiki 資料...")

    with open(wiki_input, 'r', encoding='utf-8') as f_in, \
         open(wiki_output, 'w', encoding='utf-8') as f_out:

        # 因為來源是 JSON 陣列 ["...", "..."]，直接載入為 Python List
        wiki_articles = json.load(f_in)

        # 使用 enumerate 走訪每一篇文章，並加上 index 來當作 ID
        for index, text in enumerate(wiki_articles):
            doc = {
                "id": f"wiki_{index}",  # 自動產生 ID：wiki_0, wiki_1...
                "contents": text
            }
            f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

    print(f"✅ Wiki 轉換完成！共處理 {len(wiki_articles)} 篇文章，已儲存至: {wiki_output}")
else:
    print(f"⚠️ 找不到檔案 {wiki_input}，跳過 Wiki 處理。")

print("\n🎉 所有轉換任務執行完畢！")