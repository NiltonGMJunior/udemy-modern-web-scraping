from urllib.parse import urljoin
import scrapy
from scrapy_selenium import SeleniumRequest

class ExampleSpider(scrapy.Spider):
    name = 'computerdeals'

    def start_requests(self):
        yield SeleniumRequest(
            url="https://slickdeals.net/computer-deals",
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        products = response.xpath("//ul[@class='dealTiles categoryGridDeals blueprint']/li")
        for product in products:
            yield {
                "name": product.xpath(".//div/div/div[1]/div[1]/div/a/text()").get(),
                "link": urljoin(base=response.request.url, url=product.xpath(".//div/div/div[1]/div[1]/div/a/@href").get()),
                "price": product.xpath("normalize-space(.//div/div/div[1]/div[2]/div[@class='priceLine']/div/text())").get(),
                "store_name": product.xpath(".//div/div/div[1]/div[1]/div/span[@class='blueprint']/button/text()").get(),
            }

        next_page = response.xpath("//a[@data-role='next-page']/@href").get()
        if next_page:
            absolute_url = urljoin(base=response.request.url, url=next_page)
            yield SeleniumRequest(
                url=absolute_url,
                wait_time=3,
                callback=self.parse
            )
