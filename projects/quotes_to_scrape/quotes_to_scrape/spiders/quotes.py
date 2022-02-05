import scrapy
from scrapy_splash import SplashRequest
from urllib.parse import urljoin


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
            splash.private_mode_enabled = false
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(5))
            splash:set_viewport_full()
            return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js', callback=self.parse, endpoint='execute', args={'lua_source': self.script})

    def parse(self, response):
        quotes = response.xpath("//div[@class='quote']")
        for quote in quotes:
            yield {
                "quote_text": quote.xpath(".//span[@class='text']/text()").get(),
                "author": quote.xpath(".//span/small[@class='author']/text()").get(),
                "tags": quote.xpath(".//div[@class='tags']/a/text()").getall(),
            }

        next_page = response.xpath("//li[@class='next']/a/@href").get()
        url = urljoin(response.url, next_page)
        yield SplashRequest(url=url, callback=self.parse, endpoint='execute', args={'lua_source': self.script})

