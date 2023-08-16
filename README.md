![](https://img.shields.io/badge/python-v3.9-blue)
![](https://img.shields.io/github/license/ystepanoff/updaemon)

# updaemon: monitoring web sources and getting notified

![](https://i.imgur.com/INQyb8C.png)

# Installation

```
$ git clone https://github.com/ystepanoff/updaemon
$ cd updaemon
$ mv updaemon.example.conf updaemon.conf
$ mv docker-compose.example.yaml docker-compose.yaml
```

Populate `updaemon.conf` and `docker-compose.yaml` with the relevant configuration options. Make sure the MySQL passwords in both files are the same.

```
$ docker compose build
$ docker compose up -d
```

Configure reverse proxy (below is an example Nginx configuration):

```
server {
    listen 8080;
    listen [::]:8080;

    server_name your-server;

    location / {
        proxy_pass http://127.0.0.1:5000;
        include proxy_params;
    }
}
```
