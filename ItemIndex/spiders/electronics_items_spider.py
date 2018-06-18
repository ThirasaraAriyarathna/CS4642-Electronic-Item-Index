import scrapy


class ElectronicItemsSpider(scrapy.Spider):
    name = 'electronics_items'

    start_urls = ['https://takas.lk/electronics-computers.html?___SID=U&limit=32']

    def parse(self, response):
        # follow links to item details pages
        for href in response.css('ul.products-grid li.item div.actions a::attr(href)'):
            yield response.follow(href, self.parse_electronic_item)

        href = response.css('div.pages li a.next::attr(href)')[0]
        yield response.follow(href, self.parse)

    def parse_electronic_item(self, response):
        def extract_with_css(query):
            element = response.css(query).extract_first()
            if element is not None:
                return response.css(query).extract_first().strip()
            else:
                return None

        def extract_lists(query):
            arr = response.css(query).extract()
            if arr is None:
                return []
            else:
                return arr

        def extract_lists_specific(query, key):
            arr = response.css(query).extract()
            for i in arr:
                if key in i:
                    return [i.strip()]
            return []

        yield {
            'product_name': extract_with_css('div.product-name h1::text'),
            'category': " ".join(extract_with_css('div.category-products div.block-title span::text').split()[2:]),
            'price': extract_with_css('div.price-box span.regular-price span.price::text'),
            'status': extract_with_css('p.availability span::text'),
            'short_description': extract_lists('div.short-description div.std ul li::text'),
            'warranty_period': extract_lists('div.short-description div.std p span strong::text') + extract_lists_specific('div.custom-elements ul.basic-list li::text', "Warranty"),
        }


