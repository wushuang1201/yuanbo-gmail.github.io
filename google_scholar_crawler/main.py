from scholarly import scholarly
import jsonpickle
import json
from datetime import datetime
import os

try:
    author_id = os.environ.get('GOOGLE_SCHOLAR_ID')
    if not author_id:
        raise ValueError("GOOGLE_SCHOLAR_ID环境变量未设置")

    author = scholarly.search_author_id(author_id)
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])

    # 优化数据结构
    name = author.get('name', '未知作者')
    author['updated'] = str(datetime.now())
    author['publications'] = {v['author_pub_id']: v for v in author.get('publications', [])}

    # 创建结果目录
    os.makedirs('results', exist_ok=True)

    # 保存作者数据
    with open(f'results/gs_data.json', 'w', encoding='utf-8') as outfile:
        json.dump(author, outfile, ensure_ascii=False, indent=2)

    # 为Shields.io创建数据
    shieldio_data = {
        "schemaVersion": 1,
        "label": "citations",
        "message": f"{author.get('citedby', 0)}",
    }
    with open(f'results/gs_data_shieldsio.json', 'w', encoding='utf-8') as outfile:
        json.dump(shieldio_data, outfile, ensure_ascii=False)

except Exception as e:
    print(f"处理过程中发生错误: {e}")
