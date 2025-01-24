# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:

    def process_item(self, item, spider):
        
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        for file_name in field_names:
            if file_name != 'description':
                adapter[file_name] = adapter[file_name].strip()
                
        ## Category & Product Type -> switch to lowercase
        lowercase_key = ['category', 'product_type']
        for lower_key in lowercase_key:
            adapter[lower_key] = adapter[lower_key].lower()
            
        ## Price --> convert to float
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            adapter[price_key] = float(adapter[price_key].replace('£', ''))
            
            
        ## Availability --> extract number of books in stock
        availability_string = adapter['availability']
        split_string_array = availability_string.split('(')
        if len(split_string_array) < 2:
            # Ví dụ: Out of stock
            adapter['availability'] = 0
        else:
            # Ví dụ: In stock (19 available)
            availability_string = split_string_array[1]
            availability_string = availability_string.split(' ')[0]
            adapter['availability'] = int(availability_string)
            
            
        ## Reviews --> convert string to number
        num_reviews_string = adapter['num_reviews']
        adapter['num_reviews'] = int(num_reviews_string)
        
        ## Stars --> convert text to number
        stars_string = adapter['stars']
        split_stars_array = stars_string.split(' ')
        stars_text_value = split_stars_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5
            
        return item


