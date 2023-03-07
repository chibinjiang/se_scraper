import time
from datetime import datetime

from basic_bs import BasicSC


class BingBarcodeSearcher(BasicSC):

    @property
    def headers(self):
        headers = {
            'authority': 'www.bing.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
            'sec-ch-ua-arch': '"arm"',
            'sec-ch-ua-bitness': '"64"',
            'sec-ch-ua-full-version': '"110.0.5481.177"',
            'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.177", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.177"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-model': '""',
            'sec-ch-ua-platform': '"macOS"',
            'sec-ch-ua-platform-version': '"12.5.1"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'none',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
        }
        return headers

    def search(self, mcc, keyword):
        """
        ?setlang=en&cc=vn&cc=VN
        /?setmkt=vi-vn
        :param mcc:
        :param keyword:
        :return:
        """
        params = {'q': keyword, 'PC': 'U316', 'FORM': 'CHROMN'}
        url = 'https://www.bing.com/search'
        print(f"Search {keyword} in {mcc}: {url}")
        response = self.session.get(
            url, params=params, timeout=self.timeout
        )
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
    se = BingBarcodeSearcher(interval=4)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(f"bing_results_{now}.txt", 'w') as fw:
        for mcc, barcode in se.load_barcodes():
            for result in se.search(mcc, barcode):
                fw.write(f"{mcc},{barcode},{result}\n")


if __name__ == '__main__':
    main()
