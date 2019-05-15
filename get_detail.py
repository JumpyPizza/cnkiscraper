from requests_html import HTMLSession


class GetDetail:
    def __init__(self):
        self.down_count = 'NA'
        self.org = 'NA'
        self.abstract = 'NA'
        self.keyword = 'NA'
        self.fund = 'NA'
        self.doi = "NA"
        self.classification = 'NA'
        self.reference = "NA"
        self.secrefer = "NA"
        self.cosite = "NA"

    def parsePage(self, url):
        session = HTMLSession()
        r = session.get(url)
        if r.status_code == 404:
            return None
        else:
            try:
                div = r.html.find('div.wxmain', first=True)
                # 获取下载次数
                if div.find("span.a", first=True):
                    self.down_count = div.find("span.a", first=True).find("b", first=True).text
                # 获取作者单位
                if div.find('div.orgn', first=True):
                    self.org = ""
                    orgdiv = div.find('div.orgn', first=True)
                    orgspan = orgdiv.find('span')
                    for i in orgspan:
                        self.org += i.text + "\n"
                # 获取摘要
                if div.find('span#ChDivSummary', first=True):
                    self.abstract = div.find('span#ChDivSummary', first=True).text
                # 关键词
                if div.find('a[onclick*=kw]'):
                    self.keyword = ""
                    kwordsitm = div.find('a[onclick*=kw]')
                    for i in kwordsitm:
                        self.keyword += i.text + ' '
                # 基金
                if div.find('a[onclick*=fu]'):
                    self.fund = ""
                    fuitm = div.find('a[onclick*=fu]')
                    for i in fuitm:
                        self.fund += i.text+"\n"
                # doi
                if div.xpath('//label[@id="catalog_ZCDOI"]'):
                    self.doi = div.xpath('//label[@id="catalog_ZCDOI"]/following::text()[1]')[0]
                elif div.xpath('//label[@id="catalog_DOI"]'):
                    self.doi = div.xpath('//label[@id="catalog_DOI"]/following::text()[1]')[0]
                # 分类号
                if div.xpath('//label[@id="catalog_ZTCLS"]'):
                    self.classification = div.xpath('//label[@id="catalog_ZTCLS"]/following::text()[1]')[0]

                return vars(self).items()
            except Exception as e:
                print(e)






