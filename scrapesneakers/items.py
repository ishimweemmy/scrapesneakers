import scrapy
from scrapy import Field


class AdidasSneakerItem(scrapy.Item):
    shoe_id = scrapy.Field()
    # sneaker_url = scrapy.Field()
    rating_nbr = scrapy.Field()
    name = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    discount_rate = scrapy.Field()
    callout_subtitle = scrapy.Field()
    colors = scrapy.Field()
    sizes = scrapy.Field()
    image_urls = scrapy.Field()

# class AdidasSneakerItem(scrapy.Item):
#     rating_nbr = Field()
#     name = Field()
#     old_value = Field()
#     new_value = Field()
#     discount_rate = Field()
#     callout_subtitle = Field()
#     colors = Field()
#     # sizes: available, unavailable
#     sizes = Field()
#     otherImages = Field()
#     # each review with: title, star-ratings, description, date posted, user,
#     reviews = Field()
#     sneaker_description = Field()
#     sneaker_details = Field()
