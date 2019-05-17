import copy
import time
from urllib.parse import urlparse, parse_qs
from requests_html import HTMLSession
import ast
# 获取引文网络的计数的链接
REF_COUNT_URL = 'http://kns.cnki.net/kcms/detail/block/refcount.aspx'
# 获取参考文献列表的链接
REF_INFO_URL='http://kns.cnki.net/kcms/detail/frame/list.aspx'
class GetDetail:
    def __init__(self):
        self.down_count = 'NA'
        self.org = 'NA'
        self.abstract = 'NA'
        self.keyword = 'NA'
        self.fund = 'NA'
        self.doi = "NA"
        self.classification = 'NA'
        self.reference = '0' # 参考文献
        self.refered_by = '0' # 引证文献
        self.secondrefer = '0' # 二级参考文献
        self.secondreby = '0' # 二级引证文献
        self.cosite = '0' # 共引文献
        self.cosited_by = '0' # 同被引文献


    def parsePage(self, url):
        session = HTMLSession()
        r = session.get(url)
        if r.status_code != 200:
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
                '''
                得到参考文献相关数据
                '''
                if r.html.find("div.map", first=True):
                    param_data = urlparse(url)  # 解析url
                    params_parsed = parse_qs(param_data.query)
                    params = {}
                    #  cnki得到的详情页参数怎么乱七八糟的...大小写不统一啊..
                    for key in params_parsed.keys():
                        if key.lower() == 'dbcode':
                            params['dbcode'] = params_parsed[key]
                        if key.lower() == 'dbname':
                            params['dbname'] = params_parsed[key]
                        if key.lower() == 'filename':
                            params['filename'] = params_parsed[key]

                    # 得到参数字典
                    # 构造获取参考文献计数的请求参数
                    ref_count_data = copy.copy(params)   # 浅复制，防止改变原对象
                    ref_count_data['vl'] = ""
                    try:
                        ref_count_page = session.get(REF_COUNT_URL, params=ref_count_data)
                        ref_count_dict = ast.literal_eval(ref_count_page.html.text)
                        self.reference = ref_count_dict['REFERENCE']  # 参考文献
                        self.refered_by = ref_count_dict['CITING']  # 引证文献
                        self.secondrefer = ref_count_dict['SUB_REFERENCE']  # 二级参考文献
                        self.secondreby = ref_count_dict['SUB_CITING']  # 二级引证文献
                        self.cosite = ref_count_dict['CO_CITING']  # 共引文献
                        self.cosited_by = ref_count_dict['CO_CITED']  # 同被引文献
                        # 获取参考文献和引证文献列表
                        ref_info_data = copy.copy(ref_count_data)
                        if ref_count_dict['REFERENCE'] != '0':
                            ref_info_data['RefType'] = 1  # 参考文献
                            self.reference = self.getReferList(ref_info_data)
                        if ref_count_dict['CITING'] != '0':
                            ref_info_data['RefType'] = 3 # 引证文献
                            self.refered_by = self.getReferList(ref_info_data)
                    except Exception as e:
                        print(e)
                        print("请求失败计数页失败")
                return vars(self).items()
            except Exception as e:
                print(e)
                return vars(self).items()




    def getReferList(self, param_data):
        session = HTMLSession()
        try:
            ref = session.get(REF_INFO_URL, params=param_data)
            reflist = ref.html.text.split('\n')  # 获取第1页所有文献的列表
            refset = set(reflist)  # 针对当前页面的所有文献创建集合
            ref.html.render()  # 渲染js得到翻页数
            dblist = ['CJFQ', 'CDFD', 'CMFD', 'CPFD', 'IPFD', 'CCND', 'CCJD']
            for i in dblist:
                span = ref.html.find("span[id=%s]" % i, first=True)  # 搜索页面上需要翻页的都有哪些数据库
                if span:  # 如果找到需要翻页的数据库。一般来说，如果这个为True，那么下面就能搜索到共几页
                    if span.search('共{num}页'):
                        page_num = int(span.search('共{num}页')['num'])
                        ref_page_data = copy.copy(param_data)
                        ref_page_data['CurDBCode'] = i
                        for j in range(2, page_num + 1):
                            ref_page_data['page'] = j
                            ref_change_page = session.get(REF_INFO_URL, params=ref_page_data)
                            refset = refset | set(ref_change_page.html.text.split('\n'))
                            time.sleep(1)
            referencelist = list(refset)
            for i in referencelist:
                if "[" not in i:
                    referencelist.remove(i)
            return referencelist
        except Exception as e:
            print("请求列表页失败")
            print(e)
            return "0"


if __name__ == '__main__':
    a = GetDetail().parsePage('http://kns.cnki.net/KCMS/detail/detail.aspx?QueryID=0&CurRec=11&recid=&FileName=HXGY201805003&DbName=CJFDPREP&DbCode=CJFQ&yx=Y&pr=&URLID=12.1102.TQ.20170112.1533.019&bsm=QK0202')
    for i in a:
        print(i)
