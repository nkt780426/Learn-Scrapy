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
                
        # Category & Product Type -> switch to lowercase
        lowercase_key = ['category', 'product_type']
        for lower_key in lowercase_key:
            adapter[lower_key] = adapter[lower_key].lower()
            
        return item

    
