from browser_cookie3 import chrome
from config_hgsw import WEB_HEADERS


def get_cookies():
    try:
        chrome_cookie = chrome(domain_name='84.52.16.1')
        return chrome_cookie
    except PermissionError:
        print(f"无法读取 Cookie. 必须关闭chrome浏览器才能取得JSESSIONID!")


def get_jsessionid(cookie):
    # 查找特定的cookie
    jsessionid_cookie = next((c for c in cookie if c.name == 'JSESSIONID'), None)
    if jsessionid_cookie:
        print(f"JSESSIONID: {jsessionid_cookie.value}")
        return jsessionid_cookie.value
    else:
        print("JSESSIONID not found")


def build_headers_with_jsessionid(jsessionid):
    new_headers = WEB_HEADERS.copy()
    new_headers['Cookie'] = f"JSESSIONID={jsessionid}"
    return new_headers


if __name__ == '__main__':
    cookies = get_cookies()
    new_jsessionid = get_jsessionid(cookies)
    headers = build_headers_with_jsessionid(new_jsessionid)
