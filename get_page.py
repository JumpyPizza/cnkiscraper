from requests_html import HTMLSession
from basic_config import config
import time
from urllib.parse import quote
import re
from get_detail import GetDetail

# 获取cookie
BASIC_URL = 'http://kns.cnki.net/kns/brief/result.aspx'
# 发送post请求进行注册，以便发送get请求获取搜索结果
POST_URL = 'http://kns.cnki.net/kns/request/SearchHandler.ashx'
# 发送get请求获取搜索结果
GET_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx?pagename='
# 翻页
CHANGE_PAGE_URL = 'http://kns.cnki.net/kns/brief/brief.aspx'

HEADER = config.crawl_headers


class GetPage():
    def __init__(self):
        self.session = HTMLSession()
        self.cur_page_num = 1 # 目前页码
        # 获取cookie保持会话
        self.session.get(BASIC_URL, headers = HEADER)
    # 传入搜索要用的关键字， 以及搜索条件。必须为str
    def getSearchResult(self, kword, condition):
        # 这里可以控制搜索的数据库。不作限制。
        static_post_data = {
            'action': '',
            'NaviCode': '*',
            'ua': '1.21',
            'isinEn': '1',
            'PageName': 'ASP.brief_default_result_aspx',
            'DbPrefix': 'SCDB',
            'DbCatalog': '中国学术期刊网络出版总库',
            'ConfigFile': 'SCDB.xml',
            'db_opt': 'CJFQ,CDFD,CMFD,CPFD,IPFD,CCND,CCJD',  # 搜索类别（CNKI右侧的）
            'his': '0',
            '__': time.asctime(time.localtime()) + ' GMT+0800 (中国标准时间)'
        }
        # 此处可以更改搜索参数
        search_condition = {
            '主题':'SU$%=|',
            '关键词':'KY',
            '篇名':'TI',
            '摘要':'AB',
            '全文':'FT'
        }
        u_input = {'txt_1_sel': '',
                   'txt_1_value1': '',
                   'txt_1_relation': '#CNKI_AND',
                   'txt_1_special1': '='}
        u_input['txt_1_sel'] = search_condition.get(condition)
        u_input[ 'txt_1_value1'] = kword
        post_data = dict(static_post_data, **u_input)
        # 发送post请求
        req_first = self.session.post(POST_URL, data=post_data, headers=HEADER)
        # 传入搜索的关键词
        k_v = quote(u_input.get('txt_1_value1'))
        # 构造url发送get请求，得到搜索结果列表页
        result_url = GET_PAGE_URL + req_first.text + '&t=1544249384932&keyValue=' + k_v + '&S=1&sorttype='
        req_sec = self.session.get(result_url, headers=HEADER)
        # 解析搜索结果列表页，得到标题、详情页URL、作者、来源、发表时间、数据库、被引、下载
        rows = req_sec.html.xpath('//tr[@bgcolor]')
        for row in rows:
            td = row.find('td')
            title = td[1].find('a', first=True).text
            detail_url = re.sub('/kns', 'http://kns.cnki.net/KCMS', td[1].find('a', first=True).attrs['href'])
            author = td[2].text
            journal = td[3].text
            publish_date = td[4].text
            database = td[5].text
            cite_count = row.find('span[class="KnowledgeNetcont"]', first=True)
            if cite_count:
                cite_count = cite_count.text
            else:
                cite_count = 0
        #   down_count = row.find('span[class="downloadCount"]', first=True)
        #   row是一个td，但是td的子元素中定位不到下载量，待解决。直接从chrome上copy下来的xpath也没法定位到这个元素...从详情页得到了下载量
        #   if down_count:
        #     down_count = down_count.text
        #   else:
        #     down_count = 0
        #   print(down_count)
            print(title)
            print(detail_url)
            print(author)
            print(journal)
            print(publish_date)
            print(database)
            print(cite_count)
            i = GetDetail().parsePage(detail_url)
            if i:
                for a in i:
                    print(a)

if __name__ == '__main__':
    page = GetPage()
    page.getSearchResult("电子显微镜", "主题")








