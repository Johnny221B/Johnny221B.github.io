import requests
from bs4 import BeautifulSoup
import re


def update_citation_badge():
    # 您的谷歌学术 ID
    SCHOLAR_ID = "Oj296F8AAAAJ"

    # 请求头，模拟浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # 发送请求
    url = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching data: {e}")
        return False

    # 解析 HTML 获取引用数
    soup = BeautifulSoup(response.text, 'html.parser')
    citation_stats = soup.select('td.gsc_rsb_std')
    if len(citation_stats) >= 1:
        total_citations = citation_stats[0].text
    else:
        print("Failed to find citation count")
        return False

    # 更新 index.html 中的徽章
    with open('index.html', 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式替换徽章
    # 这里保持 "Google Scholar" 作为左侧文本，引用数作为右侧
    new_badge = f'<a href=\'https://scholar.google.com/citations?user=Oj296F8AAAAJ\'>\n  <img src="https://img.shields.io/badge/Google%20Scholar-{total_citations}-blue?logo=Google%20Scholar&style=flat&labelColor=f6f6f6&color=9cf">\n</a>'
    pattern = r'<a href=\'https://scholar\.google\.com/citations\?user=Oj296F8AAAAJ\'>\s*<img[^>]*>\s*</a>'

    updated_content = re.sub(pattern, new_badge, content)

    # 写回文件
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Updated citation badge to {total_citations} citations")
    return True


if __name__ == "__main__":
    update_citation_badge()
