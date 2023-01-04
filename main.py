from checker import ProxyChecker


if __name__ == '__main__':
    proxy_path = input('Insert location of proxies: ')

    timeout = int(input('Insert the timeout (MS): '))

    url = input('Insert URL: ')

    proxy_type = input('Enter the proxy type: ')

    proxy_checker = ProxyChecker(proxy_path, timeout, url, proxy_type)

    proxy_checker.check_proxies()
