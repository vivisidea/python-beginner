#!/usr/bin/env python
# -*- encoding=utf8 -*-
#

"""
demo of the requests utils module, see http://docs.python-requests.org/en/latest/
"""

import requests
import re
import json
import hashlib
import base64
import urllib

def requestdemo():
    """
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
    :param data: (optional) Dictionary, bytes, or file-like object to send in the body of the :class:`Request`.
    :param headers: (optional) Dictionary of HTTP Headers to send with the :class:`Request`.
    :param cookies: (optional) Dict or CookieJar object to send with the :class:`Request`.
    :param files: (optional) Dictionary of 'name': file-like-objects (or {'name': ('filename', fileobj)}) for multipart encoding upload.
    :param auth: (optional) Auth tuple to enable Basic/Digest/Custom HTTP Auth.
    :param timeout: (optional) Float describing the timeout of the request.
    :param allow_redirects: (optional) Boolean. Set to True if POST/PUT/DELETE redirect following is allowed.
    :param proxies: (optional) Dictionary mapping protocol to the URL of the proxy.
    :param verify: (optional) if ``True``, the SSL cert will be verified. A CA_BUNDLE path can also be provided.
    :param stream: (optional) if ``False``, the response content will be immediately downloaded.
    :param cert: (optional) if String, path to ssl client cert file (.pem). If Tuple, ('cert', 'key') pair.

    Usage::

      >>> import requests
      >>> req = requests.request('GET', 'http://httpbin.org/get')
      <Response [200]>
    """
    url = 'http://httpbin.org/'
    r = requests.get(url)
    print r.headers['content-type'] # r.headers访问返回的头部数据
    print r.status_code # 返回状态
    print r.encoding    # 编码
    print 'headers: ', r.headers
    print 'cookies: ', r.cookies
#    print r.text        # 返回内容
#    print r.json()      # 支持直接把结果json字符串转换成json对象

    # send your own cookies
    cookies = dict(username='vivisidea')
    r = requests.get('http://httpbin.org/cookies', cookies=cookies)
    print r.text

WBCLIENT = 'ssologin.js(v.1.3.18)'
sha1 = lambda x: hashlib.sha1(x).hexdigest()
LOGINURL= 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&client=%s'

def wblogin(username, password):
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1'
    }
    resp = requests.get(
        LOGINURL % (base64.b64encode(username), WBCLIENT),
        headers = headers
    )
    pre_login_str = re.match(r'[^{]+({.+?})', resp.content).group(1)
    pre_login_json = json.loads(pre_login_str)
    data = {
        'entry': 'weibo',
        'gateway': 1,
        'from': '',
        'savestate': 7,
        'useticket': 1,
        'ssosimplelogin': 1,
        'su': base64.b64encode(urllib.quote(username)),
        'service': 'miniblog',
        'servertime': pre_login_json['servertime'],
        'nonce': pre_login_json['nonce'],
        'pcid': pre_login_json['pcid'],
        'vsnf': 1,
        'vsnval': '',
        'pwencode': 'wsse',
        'sp': sha1(sha1(sha1(password)) +
                   str(pre_login_json['servertime']) +
                   pre_login_json['nonce']),
        'encoding': 'UTF-8',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si'
               'naSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    resp = requests.post(
        'http://login.sina.com.cn/sso/login.php?client=%s' % WBCLIENT,
        data=data,
        headers=headers
    )
    login_url = re.search(r'replace\([\"\']([^\'\"]+)[\"\']',
        resp.content).group(1)
    resp = requests.get(login_url, headers=headers)
    login_str = re.match(r'[^{]+({.+?}})', resp.content).group(1)
    return json.loads(login_str)

if __name__ == '__main__':
#    requestdemo()
    print wblogin('username', 'password') # 实际上这段代码已经不能用了