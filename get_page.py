# http://yuanjian.cnki.net的搜索等于http://search.cnki.com.cn的全文检索
# search.cnki.com.cn比cnki的检索少了英文文献
# 可以爬到的具体文献的页面信息不全，新的页面怎么爬
# TODO
# 遍历页面 数据库连接 相关机构 相关期刊 异常处理
from requests_html import HTMLSession
from get_detail import GetDetail
import re

def getpage(url):
    session = HTMLSession()
    r = session.get(url)
    # 获取当前页面所有的搜索结果
    a = r.html.find('div.wz_content')

    for item in a:
        titleitm = item.find('a[target=_blank]')
        # 获取标题和链接
        title = titleitm[0].text # 这个元素中的文字
        link = list(titleitm[0].absolute_links)[0] # absolute_links获取这个元素包含的绝对路径的集合
        # 获取出版社及日期
        publisheritm = item.find('span.year-count span[title]')
        publisher = publisheritm[0].text # 其中包含出版社和日期，以空格分开。硕博士论文是"学校 论文 日期"，其它是"期刊 时间 第几期"
        publisher_split = publisher.split()
        if re.match('硕士|博士', publisher_split[1]):
          publish_house = publisher_split[0]+" "+publisher_split[1]
          publish_date = publisher_split[2]
        elif len(publisher_split) == 2:  # 会议文献
          publish_house = publisher_split[0]
          publish_date = publisher_split[1]
        else:
          publish_house = publisher_split[0]
          publish_date = publisher_split[1]+" "+publisher_split[2]
        # 获取下载量和被引量
        countitm = item.find('span.year-count span.count')
        count = countitm[0].text
        count_split = count.split("|") # 下载量|被引量
        # 获取下载次数
        d_search = re.search("[0-9]+", count_split[0])
        if d_search:
          download_count = d_search.group()
        else:
          download_count = str(0)
        # 获取被引次数
        c_search = re.search("[0-9]+", count_split[1])
        if c_search:
          cited_count = c_search.group()
        else:
          cited_count = str(0)


        print(title)
        print(publish_house)
        print(publish_date)
        print(download_count)
        print(cited_count)
        print(link)
        detail = GetDetail().parsePage(link)
        if detail:
            for a in detail:
                print(a)
