# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# # Có thể tiền xử lý dữ liệu ở đây, nếu nó đơn giản, phức tạp hơn thì khai báo function trong file pipelines
# def serialize_price(value):
#     return f'$ {str(value)}'


class BookItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    upc = scrapy.Field()
    product_type = scrapy.Field()
    # price_excl_tax = scrapy.Field(serializer = serialize_price)
    price_excl_tax = scrapy.Field()
    price_incl_tax = scrapy.Field()
    tax = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    stars = scrapy.Field()
    category = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()
