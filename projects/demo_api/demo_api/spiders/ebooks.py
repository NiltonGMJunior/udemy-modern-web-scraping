import scrapy
import json

class EbooksSpider(scrapy.Spider):
    name = 'ebooks'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=0']
    offset = 0
    incremented_by = 12

    def parse(self, response):
        # NOTE: Maybe check for resp.status_code == 200 or != 500 to stop paginating
        resp = json.loads(response.body)
        ebooks = resp.get('works')
        if ebooks:
            for ebook in ebooks:
                yield {
                    'title': ebook.get('title'),
                    'subjects': ebook.get('subject', []),
                }

            self.offset += self.incremented_by
            yield scrapy.Request(
                url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.offset}',
                callback=self.parse
            )
