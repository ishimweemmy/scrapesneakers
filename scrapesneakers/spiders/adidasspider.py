import scrapy
import uuid
from scrapesneakers.items import AdidasSneakerItem  # Import your custom item
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class AdidasspiderSpider(scrapy.Spider):
    name = "adidasspider"
    allowed_domains = ["www.adidas.com"]
    start_urls = ["https://www.adidas.com/us/lite-racer-adapt-6.0-shoes/IF7362.html"]
    
    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url, callback=self.parse, script="document.querySelector('.expand-button___3hWYb').click()", wait_time= 50, wait_until=EC.element_to_be_clickable((By.CLASS_NAME, 'expand-button___3hWYb')))

    # def parse(self, response):
    #     adidas_sneakers = response.css('div.grid-item')

    #     for adidas_sneaker in adidas_sneakers:
    #         if int(adidas_sneaker.attrib['data-index']) > -1:
    #             sneaker_relative_path = adidas_sneaker.css('a').attrib['href']

    #             ad_sneaker_url = "https://adidas.com/" + sneaker_relative_path

    #             yield SeleniumRequest(url=ad_sneaker_url, callback=self.parse_sneaker, meta={'sneaker_url': ad_sneaker_url})
    #         else:
    #             print('incompatible')

    def parse(self, response):
        # sneaker_url = response.meta['sneaker_url']
        
        ratings = response.css('.sidebar___29cCJ .product-description___1TLpA .pre-header___3bx4D .star-rating___3tUz2 .gl-star-rating .gl-star-rating__item').getall()
        rating_nbr = len(ratings)
        name = response.css('.name___120FN span::text').get()
        old_price = response.css('.price-wrapper___2Pj9R .gl-price .gl-price-item--crossed::text').extract_first(default='N/A')
        if old_price != 'N/A':
            new_price = response.css('.gl-price .gl-price-item--sale::text').extract_first() or response.css('.gl-price-item::text').get()
        else:
            new_price = response.css('.product-price___2Mip5 .price___Z74_w .price___35NVI .gl-price .gl-price-item::text').extract_first(default='N/A')
            
        discount_rate = response.css('.callout-content___V6cpN .title___35qHX span::text').extract_first(default='N/A')
        callout_subtitle = response.css('.callout-content___V6cpN .callout-subtitle___2dFcw span::text').extract_first(default='N/A')
        sizes = response.css('div[data-auto-id="size-selector"] span::text').getall()
        colors = []
        shoe_id = str(uuid.uuid4())

        image_urls = response.css('div#pdp-gallery-desktop-grid-container img')
        image_urls = [img.attrib['src'] for img in image_urls if img.attrib['src'] and not img.attrib['src'].startswith('data:')]

        for color_shoe in response.css('.color-chooser-grid___1ZBx_ a'):
            shoe_color_relative_url = color_shoe.attrib['href']
            shoe_color_url = "https://adidas.com/" + shoe_color_relative_url
            shoe_color_name = color_shoe.css('img').attrib['alt']
            shoe_img_src = color_shoe.css('img').attrib['src']
            shoe_color_id = str(uuid.uuid4())
            colors.append({'id': shoe_color_id, 'name': shoe_color_name, 'url': shoe_color_url, 'img_url': shoe_img_src})

        sneaker_item = AdidasSneakerItem(
            shoe_id=shoe_id,
            # sneaker_url=sneaker_url,
            rating_nbr=rating_nbr,
            name=name,
            old_price=old_price,
            new_price=new_price,
            discount_rate=discount_rate,
            callout_subtitle=callout_subtitle,
            colors=colors,
            sizes=sizes,
            image_urls=image_urls,
        )

        yield sneaker_item
