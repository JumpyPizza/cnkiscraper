from requests_html import HTMLSession
import re

class GetDetail:
    def __init__(self):
        self.keyword = 'NA'
        self.name = 'NA'
        self.abstract = 'NA'
        self.reference = "NA"
        self.secrefer = "NA"
        self.cosite = "NA"
        self.workplace = 'NA'
        self.fund = 'NA'
        self.classification = 'NA'
        self.diplomafrom = 'NA'
        self.diploma = 'NA'
        self.diplomadate = 'NA'

    def parsePage(self, url):
        session = HTMLSession()
        r = session.get(url)
        if r.status_code == 404:
            return None
        else:
            # 获取关键词
            keyworditm = r.html.find('meta[name="keywords"]', first=True)
            self.keyword = keyworditm.attrs['content']
            # 获取文献网页的html对象
            div = r.html
            # 获取作者名称
            self.name = ""
            names = div.find('div[style="text-align:center; width:740px; height:30px;"] a[target="_blank"]')
            for i in names:
                self.name+= i.text+' '
            # 获取摘要
            abstractitm = div.find('div[style="text-align:left;word-break:break-all"][class="xx_font"]', first=True)
            self.abstract = abstractitm.text.split('：\n')[1]
            # 获取作者单位等信息
            div2 = div.find('div[style="text-align:left;"][class="xx_font"]', first=True)
            div2text = div2.text.split('\n\n')
            dic = {}
            for i in div2text:
                if ("：\n") in i:
                    itext = i.split("：\n")
                else:
                    itext = i.split("：")
                # 把存在的信息都加进字典
                text_key = re.sub('\n', '', itext[0])  # 去掉换行符
                dic[text_key] = itext[1]
            if "作者单位" in div2.text:
                self.workplace = dic['【作者单位】']
            if "基金" in div2.text:
                self.fund = dic['【基金】']
            if "分类号" in div2.text:
                self.classification = dic['【分类号】']
            if "学位授予单位" in div2.text:
                self.diplomafrom = dic['【学位授予单位】']
            if "学位级别" in div2.text:
                self.diploma = dic['【学位级别】']
            if "学位授予年份" in div2.text:
                self.diploamdate = dic['【学位授予年份】']
            # 参考文献 —— 这里能拿到的链接是老版本的cnkispace的，最多只有十条
            if div.find("div#cankao", first=True):
                self.reference = ""
                referlist = div.find("div#cankao", first=True).find("td[width='676']")
                for i in referlist:
                    i = i.text + "\n"
                    self.reference += i
            # 二级参考文献
            if div.find("div#erjicankao", first=True):
                self.secrefer = ""
                secreferlist = div.find("div#erjicankao", first=True).find("td[width='676']")
                for i in secreferlist:
                    i = i.text + "\n"
                    self.secrefer += i
            # 共引文献
            if div.find("div#gongyin", first=True):
                self.cosite = ""
                cositelist = div.find("div#gongyin", first=True).find("td[width='676']")
                for i in cositelist:
                    i = i.text + '\n'
                    self.cosite += i
            return vars(self).items()



if __name__ == '__main__':

    i = GetDetail().parsePage('http://epub.cnki.net/grid2008/detail.aspx?filename=SLKJ201905005&dbname=DKFXPREP')
    if i:
        for a in i:
            print(a)

