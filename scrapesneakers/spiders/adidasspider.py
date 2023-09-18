import scrapy


class AdidasspiderSpider(scrapy.Spider):
    name = "adidasspider"
    allowed_domains = ["www.adidas.com"]
    start_urls = ["https://www.adidas.com/us/men-originals-shoes"]

    def parse(self, response):
        adidas_sneakers = response.css('div.grid-item')
