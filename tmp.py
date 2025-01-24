import scrapy

# Tạo spider bằng lệnh scrapy genspider bookspider books.toscrape.com
class BookspiderSpider(scrapy.Spider):
    # Tên spider
    name = "bookspider"
    # Danh sách các domain được phép crawl, trong 1 trang web có thể có rất nhiều liên kết đến rất nhiều các domain khác, kiểm soát nó bằng trường này.
    # Không đặt thì scrapy không bị giới hạn. Nên đặt để tuân thủ robot.txt của website
    allowed_domains = ["books.toscrape.com"]
    # Danh sách url bắt đầu thu thập dữ liệu
    start_urls = ["https://books.toscrape.com"]

    # Kế thừa scrapy.Spider phải ghi đè, dùng để xử lý phản hồi từ server.
    def parse(self, response):
        books = response.css('article.product_pod')
        for book in books:
            
            yield {
                'name': book.css('h3 a::text').get(),
                'title': book.css('.product_price .price_color::text').get(),
                'url': book.css('h3 a').attrib['href']
            }
        next_page = response.css('li.next a ::attr(href)').get()
        if next_page is not None:
            if 'catalogue/' in next_page:
                next_page_url = "https://books.toscrape.com/" + next_page
            else:
                next_page_url = "https://books.toscrape.com/" + 'catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)