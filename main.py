import scrapy
from scrapy.pipelines.files import FilesPipeline
import datetime
from w3lib.url import url_query_cleaner
import time

class MySpider(scrapy.Spider):

    name = 'myspider'

    #allowed_domains = []

    start_urls = ['https://losangelesapparel.net/collections/men']

    def parse(self, response):
        print('url:', response.url)

        # download files (not only images, but without converting to JPG)
        for url in response.css('button::attr(data-image)').extract():
            url = url_query_cleaner(response.urljoin(url))
            yield {'file_urls': [url]}


class RenameFilesPipeline(FilesPipeline):
    '''Pipeline to change file names - to add folder name with date and time'''

    # create it only once - when Scrapy creates instance of RenameFilesPipeline
    pattern = datetime.datetime.now().strftime('images/%Y.%m.%d-%H.%M.%S/{}')

    def file_path(self, request, response=None, info=None):
        '''Changing file name - adding folder name with date and time'''

        name = request.url.split('/')[-1]
        filename = self.pattern.format(name)
        print('filename:', filename)

        return filename

# --- run it in the same file ---

from scrapy.crawler import CrawlerProcess

c = CrawlerProcess({
    # used standard FilesPipeline (download to FILES_STORE/full)
    'ITEM_PIPELINES': {'scrapy.pipelines.files.FilesPipeline': 1},

    # 'ITEM_PIPELINES': {'__main__.RenameFilesPipeline': 1},

    # this folder has to exist before downloading
    'FILES_STORE': './img3',
})

c.crawl(MySpider)
c.start()