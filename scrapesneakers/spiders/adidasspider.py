import scrapy
import uuid
from selenium import webdriver

class AdidasspiderSpider(scrapy.Spider):
    name = "adidasspider"
    allowed_domains = ["www.adidas.com"]
    start_urls = ["https://www.adidas.com/us/men-originals-shoes"]

    def parse(self, response):
        adidas_sneakers = response.css('div.grid-item')
        
        for adidas_sneaker in adidas_sneakers:
            if int(adidas_sneaker.attrib['data-index']) > -1:
                sneaker_relative_path = adidas_sneaker.css('a').attrib['href']
                
                ad_sneaker_url = "https://adidas.com/" + sneaker_relative_path
                
                yield response.follow(ad_sneaker_url, callback = self.parse_sneaker, meta={ 'sneaker_url': ad_sneaker_url })

    def parse_sneaker(self, response):
        sneaker_url = response.meta['sneaker_url']
        rating_nbr = len(response.css('.sidebar___29cCJ .product-description___1TLpA .pre-header___3bx4D .star-rating___3tUz2 .gl-star-rating .gl-star-rating__item'))
        name = response.css('.name___120FN span::text')[1].get()
        old_price = response.css('.price-wrapper___2Pj9R .gl-price .gl-price-item--crossed::text')[1].get()
        new_price = response.css('.price-wrapper___2Pj9R .gl-price .gl-price-item--sale::text')[1].get()
        discount_rate = response.css('.callout-content___V6cpN .title___35qHX span::text').get()
        callout_subtitle = response.css('.callout-content___V6cpN .callout-subtitle___2dFcw span::text').get()
        sizes = response.css('div[data-auto-id="size-selector"] span::text').getall()
        colors = []
        shoe_id = uuid.uuid4()
        images = response.css('picture[data-testid="pdp-gallery-picture"] img::attr(src)')
        
        for color_shoe in response.css('.color-chooser-grid___1ZBx_ a'):
            shoe_color_relative_url = color_shoe.attrib['href']
            shoe_color_url = "https://adidas.com/" + shoe_color_relative_url
            shoe_color_name = color_shoe.css('img').attrib['alt']
            shoe_img_src = color_shoe.css('img').attrib['src']
            shoe_color_id = uuid.uuid4()
            colors.append({ 'id': shoe_color_id, 'name': shoe_color_name, 'url': shoe_color_url, 'img_url': shoe_img_src })
            
        yield {
                shoe_id,
                sneaker_url,
                rating_nbr,
                name,
                old_price,
                new_price,
                discount_rate,
                callout_subtitle,
                colors,
                sizes
            }
