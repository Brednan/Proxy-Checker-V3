import requests
import threading
import urllib3.exceptions


Rlock = threading.RLock()


class ProxyChecker:
    def __init__(self, proxy_path, timeout, url, proxy_type):
        self.proxy_list = self.parse_proxies(proxy_path)
        self.working_proxies = []

        self.type = proxy_type

        self.timeout = timeout
        self.url = url

        self.WORKING = 1
        self.FAILED = 0

        self.working = 0
        self.failed = 0
        self.checked = 0
        self.remaining = len(self.proxy_list)

    @staticmethod
    def parse_proxies(path_):
        f = open(path_, 'r', encoding='utf-8')
        file_content = f.read()
        f.close()

        proxy_list_raw = file_content.strip().split('\n')
        proxy_list = list(dict.fromkeys(proxy_list_raw))

        duplicate_amount = len(proxy_list_raw) - len(proxy_list)

        print(f'\nRemoved {duplicate_amount} duplicates from the list of proxies!\n')

        return proxy_list

    def check_proxies(self):
        p = 0

        while p < len(self.proxy_list):
            if threading.active_count() < 650:
                threading.Thread(target=self.check_proxy, args=(self.proxy_list[p], )).start()

                p += 1

        while threading.active_count() > 1:
            pass

        print(f'Working: {self.working} | Failed: {self.failed} | Checked: {self.checked} | Remaining: {self.remaining}     ')

        self.export_proxies()

    def check_proxy(self, proxy):
        proxy_schema = {
            'http': f'{self.type}://{proxy}',
            'https': f'{self.type}://{proxy}'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36'
        }

        try:
            result = requests.get(self.url, timeout=self.timeout/1000, proxies=proxy_schema, headers=headers)

        except requests.exceptions.RequestException:
            self.update_status(self.FAILED)

        except urllib3.exceptions.LocationParseError:
            self.update_status(self.FAILED)

        else:
            if result.status_code == 200:
                self.update_status(self.WORKING)
                self.working_proxies.append(proxy)

            else:
                self.update_status(self.FAILED)

    def update_status(self, output: int):
        with Rlock:
            if output == self.WORKING:
                self.working += 1

            elif output == self.FAILED:
                self.failed += 1

            self.checked += 1
            self.remaining = len(self.proxy_list) - self.checked

            print(f'Working: {self.working} | Failed: {self.failed} | Checked: {self.checked} | Remaining: {self.remaining}     ', end='\r')

    def export_proxies(self):
        f = open('./output.txt', 'a')

        for proxy in self.working_proxies:
            f.write(f'{proxy}:{self.type}\n')

        f.close()
