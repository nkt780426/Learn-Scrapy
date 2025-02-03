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
Nếu bị block, có thể do ta chưa chỉ định user-agent
1. Copy User-Agent String trong tab network
- Bật F12 -> Network tab -> Refesh lại trang để xem những gì mà trình duyệt đã request đến server và response của nó.
- User-agent: Trình duyệt có vai trò là gì đối với server.
2. Truy cập trang web và điền chuỗi vừa copy vào
- Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36 Edg/132.0.0.0
- https://useragentstring.com/

2:08:10