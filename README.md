# cnkiscraper
python3.7 requests-html  
参考了CyrusRenty的实现。
### 爬取页面选择

~~因为cnki.net用了一些反爬措施，解析起来比较困难，所以用了search.cnki.com.cn这个接口。
比较： yuanjian.cnki.net的搜索等于search.cnki.com.cn的全文检索；search.cnki.com.cn比cnki的检索少了英文文献。  
此外，似乎cnki在更新，现在每个文献的详细页面都是新版了，引文网络比较全，而search.cnki.com.cn点进去还是之前的版本，引文很少，有些几乎没有。
同学们有空可以研究一下cnki.net咋爬...~~~

search.cnki.com.cn的引文太不全，而且数据库也不知道全不全。因此还是直接爬cnki。
### TODO
- 翻页
- 引文
- 数据库连接
- 命令行进行参数选择
- 代理IP
- 代码部署到云服务器
- 测试引用次数、测试学位论文
- 是否需要爬英文文献？（默认爬取）

### 功能
get_page接收搜索的关键词和搜索条件，得到搜索页的结果。从返回的结果的首页抓取所有文献的**标题、作者、出版社、日期、下载量、数据库、详细页链接**。  
get_detail接收详细页链接的url，返回一个iterator，也就是GetDetail类的实例变量，包含**关键词、作者单位、摘要、基金、DOI、分类号、参考文献、二级参考文献、共引**。如果数据不存在，则为'NA'。  
basic_config保存了一些基本参数，如请求头、线程睡眠时间。    
抓取到的结果都返回到变量中，以便写数据库。

=====================================

## update
放弃使用search.cnki.com.cn接口，因为引文网络太少了。重写爬虫ing..

