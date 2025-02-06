from scrapy import Spider
from scrapy_splash import SplashRequest
import base64

class HeadlessBrowserLoginSpider(Spider):
    name = 'amazon_login'
    
    def start_requests(self):
        start_url = 'https://www.amazon.com/ap/signin?openid.page.max_auth...'
        yield SplashRequest(
            url=start_url, 
            callback=self.start_scrapping, 
            args={
                'width': 1000, 
                'lua_source': lua_script, 
                'ua': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }
        )