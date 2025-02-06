import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_playwright.page import PageMethod

# # Vấn đề 1: trang web mà nội dung của nó được sinh ra bởi javascript sau 1 thời gian
# class QuotesSpider(scrapy.Spider):
# 	name = 'quotes'

# 	def start_requests(self):
# 		url = "https://quotes.toscrape.com/js/"
# 		yield scrapy.Request(url, meta=dict(
#             playwright = True,
#             playwright_include_page = True,
#             # Đợi cho đến khi xuất hiện button next hoặc previous ở cuối page
#             playwright_page_methods = [
#                 PageMethod('wait_for_function', """
#                 () => document.querySelector('li.next a span') || document.querySelector('li.previous a span')
#             """)
#             ],
#             errback = self.errback
#         ))

# 	async def parse(self, response):
# 		# Đóng playwright lại khi không cần render nữa, giúp tiết kiệm ram (do crawl 16 request cùng lúc)
# 		page = response.meta["playwright_page"]
# 		await page.close()

# 		for quote in response.css('div.quote'):
# 			quote_item = QuoteItem()
# 			quote_item['text'] = quote.css('span.text::text').get()
# 			quote_item['author'] = quote.css('small.author::text').get()
# 			quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
# 			yield quote_item

# 		next_page = response.css('.next>a ::attr(href)').get()

# 		if next_page is not None:
# 			next_page_url = 'http://quotes.toscrape.com' + next_page
# 			yield scrapy.Request(next_page_url, meta=dict(
# 				playwright = True,
# 				playwright_include_page = True, 
# 				playwright_page_methods =[
# 					PageMethod('wait_for_selector', 'div.quote'),
# 				],
# 				errback=self.errback,
# 			))
   
# 	# Đảm bảo đóng page cho dù page có lỗi hay không
# 	async def errback(self, failure):
# 		page = failure.request.meta['playwright_page']
# 		await page.close()
  

# # Vấn đề 2: trang web mà scroll vô hạn như facebook, linkedin, et cetera, ...
# class QuotesSpider(scrapy.Spider):
# 	name = 'quotes'

# 	def start_requests(self):
# 		url = "https://quotes.toscrape.com/scroll"
# 		yield scrapy.Request(url, meta=dict(
# 			playwright = True,
# 			playwright_include_page = True,
# 			# Các PageMethod được thực hiện 1 cách tuần tự
# 			# Đợi cho đến khi 1 phần tử div.quote xuất hiện trên trang
#    			# scroll xuống cuối trang
# 			# Đợi cho đến khi phần tử div.quote thứ 11 xuất hiện trên trang
# 			playwright_page_methods =[
# 				PageMethod("wait_for_selector", "div.quote"),
# 				PageMethod("evaluate", "window.scrollBy(0, document.body.scrollHeight)"),
# 				PageMethod("wait_for_selector", "div.quote:nth-child(11)"),  # 10 per page
# 			],
#         	errback=self.errback,
# 		))

# 	async def parse(self, response):
# 		page = response.meta["playwright_page"]
# 		await page.close()

# 		for quote in response.css('div.quote'):
# 			quote_item = QuoteItem()
# 			quote_item['text'] = quote.css('span.text::text').get()
# 			quote_item['author'] = quote.css('small.author::text').get()
# 			quote_item['tags'] = quote.css('div.tags a.tag::text').getall()
# 			yield quote_item

# 	async def errback(self, failure):
# 		page = failure.request.meta["playwright_page"]
# 		await page.close()

# Vấn đề 3: chụp màn hình
class QuotesSpider(scrapy.Spider):
	name = 'quotes'

	def start_requests(self):
		url = "https://quotes.toscrape.com/js/"
		yield scrapy.Request(url, meta=dict(
			playwright = True,
			playwright_include_page = True, 
			playwright_page_methods =[
				PageMethod("wait_for_selector", "div.quote"),
			]
		))

	async def parse(self, response):
		page = response.meta["playwright_page"]
		screenshot = await page.screenshot(path="example.png", full_page=True)
		# screenshot contains the image's bytes
		await page.close()