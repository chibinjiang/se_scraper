import time
from datetime import datetime
from requests_html import HTMLSession

from geo import mcc_mapping, GOOGLE_POSTFIX_MAPPING


class BarcodeSearcher(object):

    EXCLUDE_WORDS = [
        'google.',
        'tiktok.com',
        'facebook.com',
        'twitter.com'
    ]

    def __init__(self, timeout=30, interval=1):
        self.session = HTMLSession()
        self.interval = interval
        self.timeout = timeout
        self.proxy = {
            'http': '127.0.0.1:1087',
            'https': '127.0.0.1:1087'
        }

    @property
    def headers(self):
        headers = {
            'authority': 'www.google.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'sec-gpc': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        }
        return headers

    @classmethod
    def get_google_url(cls, mcc):
        postfix = GOOGLE_POSTFIX_MAPPING['']
        if mcc_mapping.get(mcc) and mcc_mapping[mcc] in GOOGLE_POSTFIX_MAPPING:
            postfix = GOOGLE_POSTFIX_MAPPING[mcc_mapping[mcc]]
        return f"https://www.google.{postfix}/search"

    @classmethod
    def load_barcodes(cls):
        text = """
            │ 452 │ 4006465146204 │  11 │
            │ 334 │ 5160103787811 │   8 │
            │ 311 │ 017681019672  │   8 │
            │ 311 │ 035777481561  │   7 │
            │ 311 │ 681131354301  │   7 │
            │ 334 │ 3594450170064 │   7 │
            │ 310 │ 628319114081  │   7 │
            │ 208 │ 194275007410  │   7 │
            │ 452 │ 8809464014453 │   7 │
            │ 311 │ 193175442161  │   6 │
            │ 420 │ 6291003089060 │   6 │
            │ 204 │ 8710871199315 │   6 │
            │ 452 │ 8936096670020 │   6 │
            │ 420 │ 5030932124289 │   6 │
            │ 452 │ 8936036020953 │   6 │
            │ 222 │ 8015150778329 │   6 │
            │ 311 │ 883096320845  │   6 │
            │ 420 │ 6287008230231 │   6 │
            │ 262 │ 42360346      │   6 │
            │ 456 │ 8938533707078 │   6 │
            │ 334 │ 7500478018925 │   6 │
            │ 208 │ 8595011913019 │   6 │
            │ 222 │ 8944000294927 │   5 │
            │ 310 │ 842993132067  │   5 │
            │ 310 │ 195464191842  │   5 │
            │ 208 │ 887229593069  │   5 │
            │ 208 │ 8720791430658 │   5 │
            │     │ 742782421665  │   5 │
            │ 310 │ 818098021056  │   5 │
            │ 420 │ 6281101545544 │   5 │
        """
        for line in text.split("\n"):
            line = line.strip()
            tokens = [t.strip() for t in line.split("│") if t.strip()]
            if len(tokens) == 3:
                yield tokens[0], tokens[1]

    @classmethod
    def check_url_valid(cls, url):
        for word in cls.EXCLUDE_WORDS:
            if word in url:
                return False
        return True

    def search(self, mcc, keyword):
        params = {'q': keyword, 'num': 10}
        url = self.get_google_url(mcc)
        print(f"Search {keyword} in {mcc}: {url}")
        response = self.session.get(
            url, params=params, timeout=self.timeout, proxies=self.proxy
        )
        if 'did not match any documents' in response.text:
            raise Exception('No Results Found')
        elif 'Our systems have detected unusual traffic from your computer' in response.text:
            raise Exception('Captcha Triggered!\nUse Vpn Or Try After Sometime.')
        results = list()
        for ind, url in enumerate(response.html.absolute_links):
            if self.check_url_valid(url):
                print(f">>> {ind + 1}-th: {url}")
                results.append(url)
        if not results:
            print(f">>> No Search Result at all")
            return ['No Result']
        time.sleep(self.interval)
        return results


def main():
    se = BarcodeSearcher(interval=4)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"results_{now}.txt", 'w') as fw:
        for mcc, barcode in se.load_barcodes():
            for result in se.search(mcc, barcode):
                fw.write(f"{mcc},{barcode},{result}\n")


if __name__ == '__main__':
    main()
