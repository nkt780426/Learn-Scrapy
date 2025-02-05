# Nguồn
https://www.youtube.com/watch?v=mBoX_JCKZTE

# Ưu điểm
request trực tiếp hoặc beautiful shop: phù hợp với crawl data một lần, craw vài page

scrapy: 
    tích hợp nhiều tính năng hỗ trợ cào html, css, csv, json, xml, ... tốt hơn.
    hỗ trợ save vào nhiều loại source như S3, local
    tự động quay lại: nếu request lần 1 error, tự dộng retry lại.
    có thể trích xuất 
    có thể

# Mục lục

2. Cài đặt scrapy
3. Tạo scrapy project
4. Tạo spider
5. Tạo Spider negative qua các page khác nhau 
6. Làm sạch dữ liệu quá các pipeline nhỏ hơn
7. Lưu data vào đâu đó (file, database, s3, ...)
8. Fake scrapy headers và user-agents để bỏ qua một số hạn chế về trình duyệt trong một số website.
9. Rotating Proxies và Proxy APIS: ẩn IP đi 
10. Deploy spider và scheduler spiders bằng scrapyd
11. Deploy trong môi trường production: ScrapeOps và Scrapy Cloud.

# Tạo project scrapy

scrapy startproject <tên> => Tạo folder mới.

VD: scrapy startproject example

spiders: Chứa các spider.
middlewares files: Là các file cùng cấp với thư mục spiders (thường bỏ qua). Tuy nhiên file pipeline có thể được sử dụng 
    - settings.py: chứa các setting của project như kích hoạt pipelines, middlewares, thời gian delay, concurrency (đồng thời), robot.txt (cấu hình scrapy)
    - items.py: model để extract data (Các class entity)
    - pipelines.py: Thiết kế pipelines từ nguồn về đích (xử lý dữ liệu sau crawl)
    - middlewares.py: hữu dụng để thực hiện sửa đổi request và cách  scarpy chỉnh sửa reponse https
        time_out_request
        header muốn gửi: user agents
        manage_cookie_cache: 
    - scrapy.cfg: cấu hình scrapy

Có 2 loại middlewares: downloader middlewares (thường hay được sử dụng), spider middlewares. Chọn cái nào thì chỉnh trong setting.py

# Thuật ngữ
1. feed: 1 dòng dữ liệu, nội dung được cung cấp từ soure về đích (như record)
    RSS feed: Dòng tin tức hoặc bài báo từ một trang web
    Data feed: Dòng dữ liệu được cung cấp từ một hệ thống (như api hoặc db) cho ứng dụng khác
    Feed Export: Nơi dữ liệu được xuất ra (export). Trong scrapy hỗ trợ feed export ra nhiều loại như json, csv, ...

2. site = website

# Tạo spider
cd bookscraper
scrapy genspider bookspider books.toscrape.com

Truy cập vào scrapy shell bằng lệnh scrapy shell (có thể thay shell mặc định bằng ipython - nhân jupyter)

# Lệnh
1. scrapy list: liệt kê các spider
2. scrapy crawl <tên spider>: chạy 1 con nhện
    option lưu dữ liệu: 
    - thêm -O <tên file><extention> để lưu dữ liệu vào 1 file nào đó, sẽ ghi đè nếu file đã tồn tại
    - thêm -o <tên file><extention> tác dụng tương tự nhưng append vào file nếu nó đã tồn tại
    - sử dụng file setting.py

# 8. Fake User-Agent and Brower headers
Mục đích: làm cho con bot giống như đang sử dụng trình duyệt thật
User-agent: Chứa thông tin của trình duyệt, cần phải fake string này trong header của request để giả dạng trình duyệt thật. 
1. Sử dụng 1 trình duyệt với mọi request (không khuyến khích vì có thể bị chặn)
    - Copy User-Agent String trong tab network: Bật F12 -> Network tab -> Refesh lại trang để xem những gì mà trình duyệt đã request đến server và response của nó, đọc header và lấy
    - Để đọc được thông tin từ chuỗi, truy cập trang web [sau](https://useragentstring.com/) và điền User-Agent vào
2. Fake 1 user-agent mỡi mỗi request
    - Ý tưởng tạo 1 list user/agent và loop qua nó
    - Với các trang web lớn, cần phải tạo list có hàng ngàn user-agent. Hoặc sư dụng Fake User Agent API (chỉ định trong file middlewares.py)
    - [API generator User-Agent](https://scrapeops.io/?fpr=lucas37&gad_source=1&gclid=CjwKCAiAzPy8BhBoEiwAbnM9O-yfrcSfS-0rgtjGz8fmFBTEUaem4rH0MVKA6jfvCX9qKh5MLY7j6hoCpD0QAvD_BwE): Cần phải tạo tài khoản (vohoang.w2002), scrapy cung cấp free
3. Fake toàn bộ header
    - Fake user-agent là không đủ với các trang web lớn như google, amazon, ... cần phải fake toàn bộ request header cho phù hợp với broswer.
    - Sử dụng link api trên có thể làm được

# 9. Proxy
0. Các trang web proxy free 
    - https://geonode.com/free-proxy-list
    - https://free-proxy-list.net/
1. Cho mục đích học tập, tạo máy ảo:
    - Forward Proxy (proxy thuận - đại diện cho client): là máy chủ trung gian giữa client và internet. Có trách nhiệm thay mặt client gửi request đến bất kỳ đâu trong internet (router bgp chẳng hạn hay vpn). Tác dụng, che dấú ip của client (t,hường ip client là private IP thông qua bgp nên cũng chẳng cần che dấu :v), kiểm soát truy cập, lọc nội dung, caching tăng tốc độ truy cập.
    ```sh
        sudo apt install squid -y
        sudo vi /etc/squid/squid.conf
        
        # acl localnet src 192.168.56.0/24   (cho phép các máy thuộc dải mạng trên sử dụng proxy)
        # http_access allow localnet
        sudo systemctl restart squid

        # Test local, mặc định squid chỉ hỗ trợ http, cấu hình https phải thiết lập thêm
        curl -x http://192.168.56.161:3128 -I https://facebook.com
    ```
    - Reverse Proxy (proxy ngược - đại diện cho server): là máy chủ trung gian trong trình duyệt web. Nằm giữa client và các server backend (che dấu được ip server backend) và chuyển tiếp request của client đến server backend phù hợp (cân bằng tải giữa các server backend). Tác dụng cân bằng tải, bảo mật, caching, ssl termination (giải mã SSL/TTS thay cho server backend).
    - Residential Proxies: 
2. Uptime là thời gian mà một dịch vụ (như proxy) hoạt động liên tục mà không bị gián đoạn. Ví dụ, nếu một proxy có uptime 99%, điều đó có nghĩa là trong 100 giờ, proxy đó có thể sẽ ngừng hoạt động 1 giờ. Uptime càng cao thì proxy càng đáng tin cậy và ít bị gián đoạn.
3. Sử dụng project của scrapy
    pip install scrapy-rotating-proxies
4. Phương pháp 1: Liệt kê các proxy vào file setting.py
5. Phương pháp 2: Liệt kê các proxy vào file proxies.txt và thêm đường dẫn của đến file đó vào file setting.py
6. Phương pháp 3: Sử dụng service cung cấp ip và port của proxy hoạt động
    - 2 phương pháp trên đêù có nhược điểm là scrapy phải check từng proxies hoạt động hay ko. Lúc nào cũng phải lo lắng về danh sách các proxies xem nó có bị đổi ip hay ko, ...
    - service này được cung cấp bởi proxy provider và nó mất phí
    - Khi mua cần phải chú ý location. Hầu hết các trang web sẽ hoạt động khác nhau khi ở location khác nhau.

Đi xa hơn, sử dụng service có phí của scrape ops, proxy tự động cung cấp dữ liệu trang web mà ko cần phải fake user-agent hay sử dụng proxy bên thứ 3 nữa. Vẫn tài khoản đó trong scrape ops, đi vào phần proxy và xem video từ

# 10. Run spiders in cloud with scrapyd
1. Scrapyd - Free open source tool để chạy nhiều spider trên một máy chủ từ xa. 
    - Là 1 thư viện python, cần server tự tạo để chạy
    - Chỉ cung cấp api để thao tác, giao diện có thể tùy chỉnh thông qua phần mềm của bên thứ 3.
    - no scheduler
    - Cách sử dụng
    ```sh
    # Cài đặt
    pip install scrapyd -y
    # Chạy scrapyd ở chế độ backgroud
    scrapyd > scrapyd.log 2>&1 &
    # Dùng trình duyệt hoặc curl để check
    curl http://localhost:6800/daemonstatus.json
    # Cài scrapyd client cho máy chứa project và up nó lên server.
    pip install git+https://github.com/scrapy/scrapyd-client.git
    # Điều chỉnh trong file scrapy.cfg để chứa url của server (default là project name trong scrapyd)
    scrapy-deploy default
    # Project sẽ tự sinh ra các thư mục như build, project.egg-info
    # Bây giờ project đã được triển khai thành công lên scrapy và sẵn sàng để chạy
    curl http://localhost:6800/schedule.json -d project=bookscraper -d spider=bookspider
    # Dừng scrapyd
    sudo ss -tunlp (lấy pid và kill nó)
    kill <pid>
    ```

2. ScrapeOps - Free
    - Cần có server riêng tự tạo và cài scrapyd
    - Có UI
    - Có khả năng tạo jobs/spider và mornitor

3. ScrapyCloud - Paid

Triển khai scrapyd
```sh
# Trên máy server scrapyd
git clone --depth 1 https://github.com/nkt780426/Learn-Scrapy.git
sudo apt install python3.10-venv -y
python3 -m venv crawl-data
source crawl-data/bin/activate
cd cd Learn-Scrapy/
pip install -r requirements.txt

cd Learn-Scrapy/crawl-data/lib/python3.10/site-packages/scrapyd/
vi default_scrapyd.conf # Sửa bind_address thành 0.0.0.0 để chấp nhận client từ mọi nơi

# Chạy scrapyd ở chế độ background và ghi log vào file scrapyd.log thay vì in ra terminal
export SCRAPYD_BIND_ADDRESS=0.0.0.0
scrapyd > scrapyd.log 2>&1 &

# Kiểm tra status của scrapyd server từ máy client
(base) user3t@LAP027:~$ curl http://192.168.56.160:6800/daemonstatus.json
{"pending": 0, "running": 0, "finished": 0, "status": "ok", "node_name": "scrapyd"} # Không có job nào pedding, running, finished

# Package spider và up lên srapyd server
# Chỉnh url của server trong file scrapy.cfg
# Theo mặc định scrapy chỉ đóng gói các tệp scrapy lên server. Muốn nó có thêm file proxies.txt cần phải config trong setup.py
# Push spider lên server (như git)
scrapyd-deploy default
(craw_data) (base) user3t@LAP027:~/Workspace/projects/in-process/scrapy/bookscraper$ scrapyd-deploy default
Packing version 1738723310
Deploying to project "bookscraper" in http://192.168.56.160:6800/addversion.json
Server response (200):
{"project": "bookscraper", "version": "1738723310", "spiders": 1, "status": "ok", "node_name": "scrapyd"} # Project name, version push, số lượng spider trong project, status push, hostnamectl của server.
# Scheduler spider
curl http://192.168.56.160:6800/schedule.json -d project=bookscraper -d spider=bookspider
# Kiểm tra job có chạy ko
curl http://192.168.56.160:6800/listjobs.json?project=bookscraper
# Kiểm tra log
curl http://192.168.56.160:6800/logs/bookscraper/bookspider/af830432e36c11efaf13a10e0aa0ee42.log
```
Triển khai scrapydweb
```sh
pip install -r requirements.txt
# Lần đầu tiên chạy sẽ sinh ra file scrapydweb_settings_v10.py ở ~
scrapydweb
# Điều chỉnh cấu hình thành
SCRAPYD_SERVERS = [
    '127.0.0.1:6800'
]
ENABLE_LOGPARSER = True 
LOCAL_SCRAPYD_SERVER = '127.0.0.1:6800'
LOCAL_SCRAPYD_LOGS_DIR = '/home/vohoang/scrapyd/logs'
# Dừng scrapyd và start lại
mkdir scrapyd
cd scrapyd 
scrapyd > scrapyd.log 2>&1 &
# Chạy lại và tận hưởng ở port 5000 (flask)
scrapydweb > scrapydweb.log 2>&1 &
```

# 13. Recap
1. Các vấn đề còn tồn đọng
    - dynamic website: nội dung sinh ra chỉ khi di chuyển view, front-end framework chỉ hiển thị 1 phần thông tin (1 page) mà server gửi. Do đó nếu sử dụng url từ website này sẽ không nhận được data. => Scrapy pupeteer hoặc scrapy selenium
```sh
# dùng để thu thập dữ liệu từ các trang web sử dụng JavaScript động như SPA - Single Page Application. Puppeteer giúp render hoàn chỉnh trang web giúp scrapy lấy được dữ liệu sau khi JS chạy xong
pip install scrapy-puppeteer
# Thêm middleware vào puppeteer
DOWNLOADER_MIDDLEWARES = {
    'scrapy_puppeteer.middleware.PuppeteerMiddleware': 800,
}
# Tạo spider
import scrapy
from scrapy_puppeteer import PuppeteerRequest

class MySpider(scrapy.Spider):
    name = 'myspider'
    start_urls = ['https://example.com']

    async def parse(self, response):
        yield PuppeteerRequest(
            url='https://example.com',
            callback=self.parse_result
        )

    async def parse_result(self, response):
        title = response.css('title::text').get()
        yield {'title': title}
# Dùng khi trang web sử dụng nhiều js để tải nội dung hay ko thể lấy được dữ liệu vì nội dung không có trong html ban đầu, cần tương tác với trang web như click, scroll, điền form, ...
# Nếu chỉ cần lấy dữ liệu từ API ẩn trong trang thì có thể thử Scrapy + request vì puppeteer chậm hơn.
```
```sh
# scrapy-selenium cũng là middleware hỗ trợ crawl dynamic web
# selenium sử dụng webdriver thay vì puppeteer
# Dùng khi cần tương tác với web như click, scroll, điền form, đăng nhập, ...
pip install scrapy-selenium
# Cài thêm web driver nữa
DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800
}

SELENIUM_DRIVER_NAME = 'chrome'  # Hoặc 'firefox'
SELENIUM_DRIVER_EXECUTABLE_PATH = '/path/to/chromedriver'  # Đường dẫn đến WebDriver
SELENIUM_DRIVER_ARGUMENTS=['--headless']  # Chạy không hiển thị trình duyệt
# Ví dụ đơn giản
import scrapy
from scrapy_selenium import SeleniumRequest

class MySpider(scrapy.Spider):
    name = "my_spider"

    def start_requests(self):
        yield SeleniumRequest(
            url="https://example.com",
            callback=self.parse
        )

    def parse(self, response):
        title = response.css('title::text').get()
        yield {"title": title}
```

| 🛠 Công cụ         | 🌍 Trình duyệt                  | 🚀 Hiệu suất  | 🔧 Khi nào nên dùng?                                      |
|-------------------|--------------------------------|--------------|------------------------------------------------------|
| **Scrapy-Selenium**  | Chrome, Firefox, Edge, Safari... | Chậm hơn     | Khi cần tương tác với trang web (click, form...)     |
| **Scrapy-Puppeteer** | Chỉ hỗ trợ Chrome/Chromium    | Nhanh hơn    | Khi chỉ cần render JavaScript mà không cần nhiều tương tác |

Sử dụng 2 công cụ trên sẽ chạy với headless broswer (không cần ui)

2. Login endpoint
3. Scale scrape (nếu phải cào 1000 page 1 ngày thì sao)
    - Sử dụng database để lưu các url cần xử lý, sau đó dùng nhiều server

Đọc link mà khóa học recommend. scrapy-playwright đã thay thế scrapy-ppuppeteer
https://thepythonscrapyplaybook.com/freecodecamp-beginner-course/freecodecamp-scrapy-beginners-course-part-13-next-steps/