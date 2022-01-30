import scrapy


class GdpDebtSpider(scrapy.Spider):
    name = 'gdp_debt'
    allowed_domains = ['worldpopulationreview.com']
    start_urls = ['http://worldpopulationreview.com/countries/countries-by-national-debt/']

    def parse(self, response):
        countries = response.xpath("//div[contains(@class, 'datatable-container')]/table/tbody/tr")
        for country in countries:
            country_name = country.xpath(".//td[1]/a/text()").get()
            country_link = country.xpath(".//td[1]/a/@href").get()
            country_gdp_debt = country.xpath(".//td[2]/text()").get()
            country_population = country.xpath(".//td[3]/text()").get()

            yield response.follow(url=country_link, callback=self.parse_country_population, cb_kwargs={"country_name": country_name, "country_gdp_debt": country_gdp_debt, "country_population": country_population})

    def parse_country_population(self, response, country_name, country_gdp_debt, country_population):
        rows = response.xpath("//div[@id='recent-posts']/div/div[contains(@class, 'sidebar-rows')]")
        population_rank = rows.xpath(".//div[1]/div[@class='rowvalue']/a/text()").get()
        growth_rate = rows.xpath(".//div[2]/div[@class='rowvalue']/a/span/text()").get()
        world_percentage = rows.xpath(".//div[3]/div[@class='rowvalue']/span/text()").get()
        land_area = rows.xpath(".//div[5]/div[@class='rowvalue']/text()").get()

        yield {
            "country_name": country_name,
            "country_gdp_debt": country_gdp_debt,
            "country_population": country_population,
            "population_rank": population_rank,
            "growth_rate": growth_rate,
            "world_percentage": world_percentage,
            "land_area": land_area,
        }
