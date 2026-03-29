import json
import os

# 設定檔案路徑
input_file = 'Pubmed 220 Train 2022-01-21.txt'
output_dir = 'my_collection'
output_file = os.path.join(output_dir, 'pubmed_data.jsonl')

# 確保輸出資料夾存在
os.makedirs(output_dir, exist_ok=True)

current_id = None
current_contents = []

with open(input_file, 'r', encoding='utf-8') as f_in, \
     open(output_file, 'w', encoding='utf-8') as f_out:

    for line in f_in:
        line = line.strip()
        if not line:
            continue

        if line.startswith('###'):
            # 如果已經有暫存的文獻，先寫入 JSONL
            if current_id is not None:
                doc = {
                    "id": current_id,
                    "contents": " ".join(current_contents)
                }
                f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

            # 抓取新的 ID 並清空內容暫存
            current_id = line[3:]
            current_contents = []
        else:
            # 處理內文 (假設標籤和內文之間是用 Tab 或空格分開)
            # 這裡我們用 split 切割，只保留後面的實際句子內容
            parts = line.split('\t', 1)
            if len(parts) == 2:
                current_contents.append(parts[1])
            else:
                # 如果沒有 tab，則以第一個空格切割
                parts = line.split(' ', 1)
                if len(parts) == 2:
                    current_contents.append(parts[1])
                else:
                    current_contents.append(line)

    # 處理最後一筆文獻
    if current_id is not None:
        doc = {
            "id": current_id,
            "contents": " ".join(current_contents)
        }
        f_out.write(json.dumps(doc, ensure_ascii=False) + '\n')

print(f"轉換完成！檔案已儲存至 {output_file}")