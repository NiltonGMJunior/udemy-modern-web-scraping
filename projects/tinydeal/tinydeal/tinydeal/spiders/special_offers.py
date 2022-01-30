import scrapy


class SpecialOffersSpider(scrapy.Spider):
    name = 'special_offers'
    allowed_domains = ['web.archive.org']
    start_urls = [
        'https://web.archive.org/web/20190225123327/https://www.tinydeal.com/specials.html']

    def start_requests(self):
        yield scrapy.Request(url=self.start_urls[0], callback=self.parse, headers={'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'})

    def parse(self, response):
        for product in response.xpath("//ul[@class='productlisting-ul']/div/li"):
            yield {
                "title": product.xpath(".//a[@class='p_box_title']/text()").get(),
                "url": response.urljoin(product.xpath(".//a[@class='p_box_title']/@href").get()),
                "discounted_price": product.xpath(".//div[@class='p_box_price']/span[contains(@class, 'productSpecialPrice')]/text()").get(),
                "original_price": product.xpath(".//div[@class='p_box_price']/span[contains(@class, 'normalprice')]/text()").get(),
                "User-Agent": response.request.headers['User-Agent'],
            }

        next_page = response.xpath("//a[@class='nextPage']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse, headers={'User-Agent': 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0'})
