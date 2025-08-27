# Cài miniconda
- Cài vào /opt/miniconda3 để mọi user có thể nhìn thấy, sau chạy conda init --all thì thêm phần sinh ra vào /etc/bashrc để mọi user có thể có conda
- Tạo môi trường ảo craw_data

# Cài scrapyd
0. Cài 
```sh
conda activate craw_data
pip install scrapy scrapyd scrapyd-client
```
1. Thêm cấu hình sau vào /etc/scrapyd/scrapyd.conf
```sh
[scrapyd]
bind_address = 0.0.0.0
http_port   = 6800
max_proc    = 0
max_proc_per_cpu = 4
eggs_dir    = /var/lib/scrapyd/eggs
dbs_dir     = /var/lib/scrapyd/dbs
items_dir   = /var/lib/scrapyd/items
logs_dir    = /var/log/scrapyd


# Mặc định bind_address là localhost ko thể truy cập được từ bên ngoài
# max_proc: Đây là giới hạn tổng số tiến trình spider mà Scrapyd được phép chạy cùng lúc. Nếu đặt 0 nghĩa là không giới hạn
# max_proc_per_cpu: Đây là số tiến trình spider tối đa trên mỗi CPU core.

pip install logparser
/opt/miniconda3/envs/craw_data/lib/python3.10/site-packages/logparser/settings.py
```
2. Tạo các thư mục cấu hình 
```sh
sudo mkdir -p /var/lib/scrapyd/eggs /var/lib/scrapyd/dbs /var/lib/scrapyd/items /var/log/scrapyd
sudo chown -R root:root /var/lib/scrapyd /var/log/scrapyd
```
3. Mở port 6800
```sh
sudo firewall-cmd --add-port=6800/tcp --permanent
sudo firewall-cmd --reload
# Kiểm tra lại
sudo firewall-cmd --list-ports
```
3. Chạy thử truy cập vào port 6800 từ bên ngoài kiểm tra xem có giao diện ko
```sh
scrapyd
```
4. Tạo service systemd
```sh
sudo vi /usr/lib/systemd/system/scrapyd.service

[Unit]
Description=Scrapyd Daemon
After=network.target

[Service]
Type=simple
User=root
Group=root
WorkingDirectory=/root
ExecStart=/opt/miniconda3/envs/craw_data/bin/scrapyd
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable scrapyd
sudo systemctl start scrapyd
```

# Cài scrapyd web
0. Cài
```sh
pip install scrapydweb
mkdir -p /opt/scrapydweb
scrapydweb (chaỵ lần đầu sẽ sinh ra file scrapydweb_settings_v11.py, vào chỉnh)

BIND_ADDRESS = "0.0.0.0"
WEB_PORT = 5000

SCRAPYD_SERVERS = [
    'http://192.168.56.201:6800',
    'http://192.168.56.202:6800',
    'http://192.168.56.203:6800',
]

ENABLE_MONITOR = True
```
1. service systemd
```sh
sudo vi /usr/lib/systemd/system/scrapydweb.service

[Unit]
Description=ScrapydWeb Management UI
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/scrapydweb
ExecStart=/opt/miniconda3/envs/craw_data/bin/scrapydweb
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl enable scrapydweb
sudo systemctl restart scrapydweb
sudo systemctl status scrapydweb
```
2. Mở port 5000
```sh
sudo firewall-cmd --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
```