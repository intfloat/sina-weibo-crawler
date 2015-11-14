# -*- coding: utf-8 -*-
import requests
import json, re
import os
import urllib, urllib2, cookielib
from bs4 import BeautifulSoup
from copy import deepcopy

RED_V, BLUE_V, VIP, ACTIVE = 'RED_V', 'BLUE_V', 'VIP', 'ACTIVE'
verify_table = {'http://u1.sinaimg.cn/upload/2011/07/28/5338.gif': RED_V,
                'http://u1.sinaimg.cn/upload/2011/07/28/5337.gif': BLUE_V,
                'http://u1.sinaimg.cn/upload/h5/img/hyzs/donate_btn_s.png': VIP,
                'http://u1.sinaimg.cn/upload/2011/08/16/5547.gif': ACTIVE}
headers = { \
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8', \
        'Accept-Encoding':'gzip, deflate, sdch', \
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6,pl;q=0.4,zh-TW;q=0.2,ru;q=0.2', \
        'Connection':'keep-alive', \
        'Cookie':'', \
        'Host':'weibo.cn', \
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.132 Safari/537.36' \
    }
ALL, ORIGINAL = 0, 1
class WCrawler:
    def __init__(self,  cookie = None, \
                        max_num_weibo = 10, \
                        max_num_fans = 10, \
                        max_num_follow = 10, \
                        wfilter = ORIGINAL):
        self.headers = headers
        self.login_email = None
        self.password = None
        if cookie != None and len(cookie) > 0:
            self.headers['Cookie'] = cookie
        else:
            self.headers['Cookie'] = self.__get_cookie()
        self.max_num_weibo = max_num_weibo
        self.max_num_fans = max_num_fans
        self.max_num_follow = max_num_follow
        self.wfilter = wfilter
        self.data = None

    def crawl(self, url = 'http://weibo.cn/yaochen'):
        self.data = {'url': '', \
                    'nickname': '', \
                    'verify_type': '', \
                    'verify_info': '', \
                    'num_weibo': -1, \
                    'num_fans': -1, \
                    'num_follow': -1, \
                    'gender': '', \
                    'birthday': '', \
                    'weibo': [], \
                    'fans': [], \
                    'follow': [], \
                    'location': '', \
                    'relationship_status': '', \
                    'sexual_orientation': '', \
                    'self-intro': '', \
                    'tags': []
                    }
        self.data['url'] = self.__normalize_url(url)

        # step 1: crawl weibo text
        turl = self.data['url']
        if self.wfilter == ORIGINAL: turl += '?filter=1'
        req = self.__get_request(turl)
        soup = BeautifulSoup(req.text, 'lxml')
        n_page = self.__parse_max_pages(soup)
        self.data['weibo'] = self.__parse_weibo(soup)
        self.data['verify_type'] = self.__parse_user_verify_type(soup)
        info_url = self.__parse_info_url(soup)
        fans_url, follow_url = self.__parse_fans_and_follow_url(soup)
        # page by page
        for i in xrange(2, 1 + n_page):
            if len(self.data['weibo']) >= self.max_num_weibo:
                break
            turl = self.data['url'] + '?page=' + str(i)
            if self.wfilter == ORIGINAL: turl = self.data['url'] + '?filter=1&page=' + str(i)
            req = self.__get_request(turl)
            soup = BeautifulSoup(req.text, 'lxml')
            self.data['weibo'] += self.__parse_weibo(soup)
        self.data['weibo'] = self.data['weibo'][:self.max_num_weibo]

        # step 2: crawl user's personal information
        req = self.__get_request(info_url)
        soup = BeautifulSoup(req.text, 'lxml')
        self.__parse_info_list(soup)

        # step 3: crawl user's fans list
        req = self.__get_request(fans_url)
        soup = BeautifulSoup(req.text, 'lxml')
        fans_max_page = self.__parse_max_pages(soup)
        self.data['fans'] += self.__parse_fans(soup)
        for i in xrange(2, 1 + fans_max_page):
            if len(self.data['fans']) >= self.max_num_fans:
                break
            req = self.__get_request(fans_url + '?page=' + str(i))
            soup = BeautifulSoup(req.text, 'lxml')
            self.data['fans'] += self.__parse_fans(soup)
        self.data['fans'] = self.data['fans'][:self.max_num_fans]

        # step 4: crawl user's follow list
        req = self.__get_request(follow_url)
        soup = BeautifulSoup(req.text, 'lxml')
        follow_max_page = self.__parse_max_pages(soup)
        self.data['follow'] += self.__parse_follow(soup)
        for i in xrange(2, 1 + follow_max_page):
            if len(self.data['follow']) > self.max_num_follow:
                break
            req = self.__get_request(follow_url + '?page=' + str(i))
            soup = BeautifulSoup(req.text, 'lxml')
            self.data['follow'] += self.__parse_follow(soup)
        self.data['follow'] = self.data['follow'][:self.max_num_follow]

        # step 5: return final result
        return json.dumps(self.data, ensure_ascii = False, sort_keys = True, indent = 4).encode('utf-8', 'replace')

    def __parse_follow(self, soup):
        ret = []
        for table in soup.find_all('table'):
            cur = {'url': '', 'nickname': '', 'num_fans': -1}
            cur['url'] = table.find_all('a')[0]['href']
            cur['nickname'] = table.find_all('a')[1].get_text()
            for e in table.find_all('td'):
                for ch in e.children:
                    try:
                        if ch.startswith(u'粉丝'):
                            cur['num_fans'] = int(ch.strip(u'粉丝').strip(u'人'))
                    except:
                        continue
            ret.append(cur)
        return ret

    def __parse_info_list(self, soup):
        arr = soup.find_all('div')
        table = None
        for i in xrange(len(arr)):
            if arr[i]['class'][0] == 'tip' and arr[i].get_text() == u'基本信息':
                assert(i + 1 < len(arr))
                table = arr[i + 1]
        assert(table != None)
        for c in table.children:
            try:
                if c['href'].find('keyword') > 0:
                    self.data['tags'].append(c.get_text())
            except:
                pass # do nothing...
            pos = c.find(':')
            if pos < 0 or pos + 1 == len(c):
                continue
            key, val = c[:pos], c[pos + 1:]
            assert(len(key) > 0 and len(val) > 0)
            if key == u'昵称': self.data['nickname'] = val
            elif key == u'性别': self.data['gender'] = val
            elif key == u'地区': self.data['location'] = val
            elif key == u'生日': self.data['birthday'] = val
            elif key == u'简介': self.data['self-intro'] = val
            elif key == u'性取向': self.data['sexual_orientation'] = val
            elif key == u'认证': self.data['verify_info'] = val
            elif key == u'感情状况': self.data['relationship_status'] = val
            else: print 'Not include attribute:', key, val

    def __parse_fans_and_follow_url(self, soup):
        table = soup.find_all('div', attrs = {'class': 'tip2'})[0]
        fans_url, follow_url = None, None
        for e in table.children:
            try:
                text = e.get_text()
                if text.startswith(u'微博'):
                    self.data['num_weibo'] = int(text.strip(u'微博|[|]'))
                elif text.startswith(u'关注'):
                    self.data['num_follow'] = int(text.strip(u'关注|[|]'))
                    follow_url = self.__remove_qmark('http://weibo.cn' + e['href'])
                elif text.startswith(u'粉丝'):
                    self.data['num_fans'] = int(text.strip(u'粉丝|[|]'))
                    fans_url = self.__remove_qmark('http://weibo.cn' + e['href'])
            except:
                continue
        assert(follow_url != None and fans_url != None)
        return fans_url, follow_url

    def __parse_info_url(self, soup):
        table = soup.find_all('table')[0]
        for e in table.find_all('a'):
            if e.get_text() == u'资料':
                assert(e['href'][0] == '/')
                ret = 'http://weibo.cn' + e['href']
                return self.__remove_qmark(ret)
        raise 'Error: can not find info tag.'

    # def __get_cookie(self):
    #     ck = cookielib.CookieJar()
    #     opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(ck))
    #     urllib2.install_opener(opener)
    #     page = opener.open("http://3g.sina.com.cn/prog/wapsite/sso/login.php")
    #     data = page.read()
    #     password = re.findall('<postfield name="([\S]*)" value="\$\(password\)" />',data)[0]
    #     vk = re.findall('<postfield name="vk" value="([\S]*)" />',data)[0]
    #     params = urllib.urlencode({"mobile": self.login_email, \
    #                                 password: self.password, \
    #                                 "vk": vk, \
    #                                 "remember": "on", \
    #                                 "backURL": "http://weibo.cn", \
    #                                 "submit": "1"})
    #     header = {"Content-Type": "application/x-www-form-urlencoded",
    #                 "Referer": "http://3g.sina.com.cn/prog/wapsite/sso/login.php",
    #                 "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0"
    #             }
    #     req = urllib2.Request("http://3g.sina.com.cn/prog/wapsite/sso/login.php", params, header)
    #     page = urllib2.urlopen(req)
    #     print page.read()
    #     ret = ""
    #     for item in ck:
    #         ret += (item.name + '=' + item.value + ';')
    #     return ret

    def __get_request(self, url, max_try = 3):
        cnt = 0
        while cnt < max_try:
            try:
                req = requests.get(url, headers = self.headers)
            except:
                cnt += 1
                continue
            if req.status_code != requests.codes.ok:
                break
            return req
        # Should not reach here if everything is ok.
        print json.dumps(self.data, ensure_ascii = False, sort_keys = True, indent = 4).encode('utf-8', 'replace')
        print 'Error:', url
        assert(False)

    def __parse_weibo(self, soup):
        # return all weibo in a page as a list
        ret = []
        for block in soup.find_all('div', 'c'):
            divs = block.find_all('div')
            if len(divs) == 1:
                text = self.__trim_like(divs[0].get_text())
                ret.append(text)
            elif len(divs) == 2 or len(divs) == 3:
                text = self.__trim_like(divs[0].get_text())
                comment = self.__trim_like(divs[-1].get_text())
                ret.append(text + comment)
            elif len(divs) == 0:
                continue
            else:
                assert(False)
        return ret

    def __parse_max_pages(self, soup):
        # return total number of pages for one's weibo
        try:
            res = int(soup.find(id='pagelist').get_text().split('/')[-1].strip(u'页'))
        except:
            return 1
        return res

    def __parse_user_verify_type(self, soup):
        r = soup.find_all('div', attrs = {'class': 'ut'})[0].find_all('img', attrs = {'alt': 'V'})
        if len(r) == 0:
            return ''
        src = r[0]['src']
        if src in verify_table:
            return verify_table[src]
        return ''

    def __parse_fans(self, soup):
        res = []
        for follow in soup.find_all('table'):
            cur = {'url': '', 'verify_info': '', 'num_fans': -1, 'nickname': ''}
            person = follow.find_all('td')[1]
            cur['url'] = person.find('a')['href']
            img = person.find_all('img')
            if len(img) > 0:
                src = img[0]['src']
                if src in verify_table:
                    cur['verify_info'] = verify_table[src]
            pos = person.get_text().rfind(u'粉丝')
            plain = person.get_text()
            cur['nickname'] = plain[0:pos]
            cur['num_fans'] = int(plain[pos + len(u'粉丝'):].split(u'人')[0])
            res.append(cur)
        return res

    def __trim_like(self, s):
        pos = s.rfind(u'赞')
        if pos >= 0:
            return s[:pos]
        else:
            return s

    def __remove_qmark(self, url):
        while url.find('?') >= 0:
            url = url[:url.find('?')]
        return url

    def __normalize_url(self, url):
        url = self.__remove_qmark(url)
        url = url.strip('/')
        url = url.replace('weibo.com', 'weibo.cn')
        return url
