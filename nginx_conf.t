upstream backend {
	server 127.0.0.1:8000;
}

proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=all:5m max_size=50m;


server {
	listen 80;
	
	location / {
                proxy_pass http://127.0.0.1:81;
                proxy_cache all;
                proxy_cache_valid any 10m;
        }
}

server {
	listen 81;
	server_name ask.me;

	gzip on;
	gzip_min_length 1024;
	gzip_types text/css text/plain text/json text/x-js text/javascript text/xml application/json application/x-javascript application/xml application/xml+rss application/javascript;
	gzip_http_version 1.0;
	gzip_proxied any;
	gzip_disable "msie6";

        location /static/ {
                root /home/one/projects/askme/ask_tgarifullin;
                expires 1h;
        }
        location /uploads/ {
                root /home/one/projects/askme/ask_tgarifullin;
        }
#	location ~*\.\w\w\w?\w?$ {
#		root /home/one/projects/askme;
#	}
	location / {
		proxy_pass http://backend;
	}

}