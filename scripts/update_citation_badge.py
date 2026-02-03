import requests
from bs4 import BeautifulSoup
import re

USER_SCHOLAR_ID = "IFBha3gAAAAJ"  
INDEX_FILE = "index.html"            
TIMEOUT = 12


def update_citation_badge():
    url = f"https://scholar.google.com/citations?user={USER_SCHOLAR_ID}&hl=en"
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/123.0.0.0 Safari/537.36")
    }

    try:
        resp = requests.get(url, headers=headers, timeout=TIMEOUT)
        resp.raise_for_status()
    except Exception as e:
        print(f"[ERR] Fetch scholar page failed: {e}")
        return False

    soup = BeautifulSoup(resp.text, "html.parser")
    cells = soup.select("td.gsc_rsb_std")
    if not cells:
        print("[ERR] Cannot find citation cells on page.")
        return False
    total_citations = cells[0].get_text(strip=True)

    try:
        with open(INDEX_FILE, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[ERR] Read {INDEX_FILE} failed: {e}")
        return False

    badge = (
        f"<a href='https://scholar.google.com/citations?user={USER_SCHOLAR_ID}'>\n"
        f'  <img src="https://img.shields.io/badge/Google%20Scholar-{total_citations}-blue'
        f'?logo=Google%20Scholar&style=flat&labelColor=f6f6f6&color=9cf">\n'
        f"</a>"
    )

    id_escaped = re.escape(USER_SCHOLAR_ID)
    pattern = rf"<a href=['\"]https://scholar\.google\.com/citations\?user={id_escaped}['\"]>\s*<img[^>]*>\s*</a>"

    if not re.search(pattern, content, flags=re.S):
        pattern = r"<a href=['\"]https://scholar\.google\.com/citations\?user=[^'\"\s]+['\"]>\s*<img[^>]*>\s*</a>"

    new_content, n = re.subn(pattern, badge, content, flags=re.S)
    if n == 0:
        print("[WARN] No existing badge matched. Will append a new badge at placeholder <!--SCHOLAR_BADGE--> if present.")
        # 可选：如果页面里有占位注释，就在那插入；否则不处理
        if "<!--SCHOLAR_BADGE-->" in content:
            new_content = content.replace("<!--SCHOLAR_BADGE-->", badge)
            n = 1

    if n > 0:
        with open(INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[OK] Updated citation badge → {total_citations}")
        return True

    print("[ERR] Did not replace or insert badge.")
    return False


if __name__ == "__main__":
    update_citation_badge()
