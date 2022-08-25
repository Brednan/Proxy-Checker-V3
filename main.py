from checker import ProxyChecker


if __name__ == '__main__':
    proxy_path = input('Insert location of proxies: ')

    timeout = int(input('Insert the timeout: '))

    url = input('Insert URL: ')

    proxy_checker = ProxyChecker(proxy_path, timeout, url)

    proxy_checker.check_proxies()
