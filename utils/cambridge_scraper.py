import requests
from bs4 import BeautifulSoup

def get_word_info(word):
    url = f"https://dictionary.cambridge.org/zht/詞典/英語-漢語-繁體/{word}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # 音標擷取
    try:
        pron_dj = soup.select_one(".uk.dpron-i .ipa").text.strip()
    except:
        pron_dj = ""

    try:
        pron_kk = soup.select_one(".us.dpron-i .ipa").text.strip()
    except:
        pron_kk = ""

    definitions = []

    for block in soup.select(".def-block"):
        # 僅抓「定義」區塊中的中文翻譯
        zh_meaning_tags = block.select("div.def-body > span.trans")
        zh_meanings = [tag.text.strip() for tag in zh_meaning_tags]
        meaning = "；".join(zh_meanings)

        examples = []
        for ex in block.select("div.examp.dexamp"):
            en_tag = ex.select_one("span.eg")
            zh_tag = ex.select_one("span.trans")
            ex_en = en_tag.text.strip() if en_tag else ""
            ex_zh = zh_tag.text.strip() if zh_tag else ""
            if ex_en:
                examples.append({"en": ex_en, "zh": ex_zh})

        if meaning or examples:
            definitions.append({
                "meaning": meaning,
                "examples": examples
            })

    return {
        "word": word,
        "DJ": pron_dj,
        "KK": pron_kk,
        "definitions": definitions
    }
