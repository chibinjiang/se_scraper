import time
from datetime import datetime

from basic_bs import BasicSC
from geo import mcc_mapping, GOOGLE_POSTFIX_MAPPING


class GoogleBarcodeSearcher(BasicSC):

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
    se = GoogleBarcodeSearcher(interval=4)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"google_results_{now}.txt", 'w') as fw:
        for mcc, barcode in se.load_barcodes():
            for result in se.search(mcc, barcode):
                fw.write(f"{mcc},{barcode},{result}\n")


if __name__ == '__main__':
    main()
