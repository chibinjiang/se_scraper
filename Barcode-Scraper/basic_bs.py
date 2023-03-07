import re
from requests_html import HTMLSession


class BasicSC(object):

    SPECIAL_DOMAIN = [
        r'\w+\.gov',
        r'\w+\.edu',
        r'\.txt$',
        r'\.pdf$',
        r'\.png$',
        r'\.jpg$',
        r'\.jpeg$',
    ]

    EXCLUDE_WORDS = [
        'google.',
        'bing.com',
        'microsoft.com',
        'bank-code.net',
        'nomorobo.com',
        'toyota.com',
        'usbanklocations.com',
        'deltacommunitycu.com',
        'creditunionsonline.com',
        'upcindex.com',
        'ean-search.org',
        'agrusslawfirm.com',
        'youtube.com',
        'whitepages.com',
        'device.report',
        'manuals.plus',
        'northlakegastro.com',
        'tech-entrance.com',
        'canadapost.ca',
        'tiktok.com',
        'facebook.com',
        'twitter.com',
        'lachc.com',
        'shohozgroup.com',
    ]

    def __init__(self, timeout=30, interval=1):
        self.session = HTMLSession()
        self.interval = interval
        self.timeout = timeout
        self.proxy = {
            'http': '127.0.0.1:1087',
            'https': '127.0.0.1:1087'
        }

    @classmethod
    def check_url_valid(cls, url):
        """
        过滤 http://splibraries.org/
        :param url:
        :return:
        """
        for word in cls.EXCLUDE_WORDS:
            if word in url:
                return False
        for pattern in cls.SPECIAL_DOMAIN:
            if re.search(pattern, url):
                return False
        temp = url.replace("https://", "").replace("http://", "").strip("/")
        if temp.count("/") < 1:
            return False
        return True

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



