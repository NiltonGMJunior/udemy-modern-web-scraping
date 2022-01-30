import scrapy


class GlassesSpider(scrapy.Spider):
    name = 'glasses'
    allowed_domains = ['www.glassesshop.com']
    start_urls = ['https://www.glassesshop.com/bestsellers']

    def parse(self, response):
        items = response.xpath("//div[contains(@class, 'product-list-item')]")
        for item in items:
            data_element = item.xpath(".//div[@class='p-title-block']/div[@class='mt-3']/div")[0]
            yield {
                "product_image_link": item.xpath(".//div[@class='product-img-outer']/a/img/@data-src").get(),
                "product_name": data_element.xpath(".//div[1]/div[@class='p-title']/a[contains(@class, 'product-title')][1]/@title").get(),
                "product_url": data_element.xpath(".//div[1]/div[@class='p-title']/a[contains(@class, 'product-title')][1]/@href").get(),
                "product_price": data_element.xpath(".//div[2]/div[@class='p-price']/div[1]/span/text()").get(),
            }

        next_page = response.xpath("//a[text()='Next']/@href").get()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse)
