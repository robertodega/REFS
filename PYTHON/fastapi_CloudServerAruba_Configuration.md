# system access
- SSH access

# system update
- sudo apt update && sudo apt upgrade -y

# Python, pip and Nginx installation
- sudo apt install python3-pip python3-venv nginx -y

# project folder creation
- mkdir ~/my_fastapi_app && cd ~/my_fastapi_app

# virtual environment creation and activation
- python3 -m venv venv
- source venv/bin/activate

# FastAPI, Uvicorn and SQLAlchemy installation
- pip install fastapi uvicorn sqlalchemy pandas psycopg2-binary pymysql

# FastAPI engine start
- sudo nano /etc/systemd/system/fastapi.service 

        #   user= root | ubuntu

        [Unit]
        Description=Gunicorn instance to serve FastAPI
        After=network.target

        [Service]
        User=root
        Group=www-data
        WorkingDirectory=/root/my_fastapi_app
        Environment="PATH=/root/my_fastapi_app/venv/bin"
        ExecStart=/root/my_fastapi_app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

        [Install]
        WantedBy=multi-user.target

# service activation
- sudo systemctl start fastapi
- sudo systemctl enable fastapi

# Nginix configuration
- sudo nano /etc/nginx/sites-available/fastapi

        server {
            listen 80;
            server_name il_tuo_ip_o_dominio;

            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }

# configuration actvation
- sudo ln -s /etc/nginx/sites-available/fastapi /etc/nginx/sites-enabled
- sudo nginx -t
- sudo systemctl restart nginx

