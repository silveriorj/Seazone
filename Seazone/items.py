# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


class SeazoneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AIRBNB_J(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    stars = scrapy.Field()

class JurereItemLoader(ItemLoader):

    default_input_processor = TakeFirst()
    default_output_processor = TakeFirst()