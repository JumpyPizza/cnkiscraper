class LazyProperty():
    """
    LazyProperty
    加上之后，调用类中的方法时可以将其当成属性调用，而且延迟初始化，
    只在第一次调用时进行计算
    """

    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = self.func(instance)
            setattr(instance, self.func.__name__, value)
            return value

class BasicConfig():
    """
    保存Header信息
    """

    @LazyProperty
    def crawl_headers(self):
        headers = {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Host':
            'kns.cnki.net',
            'Connection':
            'keep-alive',
            'Cache-Control':
            'max-age=0',
        }
        return headers


    @LazyProperty
    def crawl_stepWaitTime(self):
        return int(self.conf.get('crawl', 'stepWaitTime'))


config = BasicConfig()