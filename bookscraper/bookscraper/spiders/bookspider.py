import scrapy
from bookscraper.items import BookItem

# Tạo spider bằng lệnh scrapy genspider bookspider books.toscrape.com
class BookspiderSpider(scrapy.Spider):
    # Tên spider
    name = "bookspider"
    # Danh sách các domain được phép crawl, trong 1 trang web có thể có rất nhiều liên kết đến rất nhiều các domain khác, kiểm soát nó bằng trường này.
    # Không đặt thì scrapy không bị giới hạn. Nên đặt để tuân thủ robot.txt của website
    allowed_domains = ["books.toscrape.com"]
    # Danh sách url bắt đầu thu thập dữ liệu (là url page 0)
    start_urls = ["https://books.toscrape.com"]

    # # Ghi đè cấu hình trong file settings.py, hiển nhiên ở đây có mức độ ưu tiên cao nhất.
    # custom_settings = {
    #     'FEEDS': {
    #         'bookdata.json': {'format': 'json', 'overwrite': True},
    #     }
    # }
    # Kế thừa scrapy.Spider phải ghi đè, dùng để xử lý phản hồi từ server.
    def parse(self, response):
        # Extract tất cả các books trong page
        books = response.css('article.product_pod')
        for book in books:
            relative_url = book.css('h3 a ::attr(href)').get()
            
            if 'catalogue/' in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/" + "catalogue/" + relative_url
                
            yield response.follow(book_url, callback = self.parse_book_page)
        
        # Nếu hết books, thực hiện di tuyển sang page tiếp theo
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/" + "catalogue/" + next_page
            yield response.follow(next_page_url, callback = self.parse)
    
    # Extract dữ liệu từng book  
    def parse_book_page(self, response):
        # Lặp qua table
        table_rows = response.css('table tr')
        book_item = BookItem()
        
        book_item['url'] = response.url
        book_item['title'] = response.css(".product_main  h1::text").get()
        book_item['upc'] = table_rows[0].css("td ::text").get()
        book_item['product_type'] = table_rows[1].css("td ::text").get()
        book_item['price_excl_tax'] = table_rows[2].css("td ::text").get()
        book_item['price_incl_tax'] = table_rows[3].css("td ::text").get()
        book_item['tax'] = table_rows[4].css("td ::text").get()
        book_item['availability'] = table_rows[5].css("td ::text").get()
        book_item['num_reviews'] = table_rows[6].css("td ::text").get()
        book_item['stars'] = response.css("p.star-rating").attrib['class']
        
        # Thường sẽ có những tag không có id, class hay thuộc tính nào như thẻ chứa category và description. Để lấy được nó dễ dàng thường ta sẽ lọc anh chị em cùng cấp với nó (sibling) mà có các thuộc tính id, class đặc biệt rồi di chuyển đến thẻ đó. Những lúc như này nên sử dụng xpath thay reponse.css()
        book_item['category'] = response.xpath("//ul[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get()
        book_item['description'] = response.xpath("//div[@id='product_description']/following-sibling::p/text()").get()
        book_item['price'] = response.css("p.price_color ::text").get()
        
        yield book_item