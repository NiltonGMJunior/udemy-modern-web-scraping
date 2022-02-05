import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com']
    user_agent = 'Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'

    def start_requests(self):
        yield scrapy.Request(
            url='http://books.toscrape.com',
            headers={
                'User-Agent': self.user_agent,
            }
        )

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//article[@class='product_pod']/h3/a"),
             callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths="//li[@class='next']/a")),
    )

    def set_user_agent(self, request, spider):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            "title": response.xpath("//div[@class='col-sm-6 product_main']/h1/text()").get(),
            "price": response.xpath("//p[@class='price_color']/text()").get(),
        }
