# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class AdidasSneakerItem(scrapy.Item):
    rating_nbr = Field()
    name = Field()
    old_value = Field()
    new_value = Field()
    discount_rate = Field()
    callout_subtitle = Field()
    colors = Field()
    # sizes: available, unavailable
    sizes = Field()
    otherImages = Field()
    # each review with: title, star-ratings, description, date posted, user,
    reviews = Field()
    sneaker_description = Field()
    sneaker_details = Field()
    