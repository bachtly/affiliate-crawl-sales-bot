# Loki + Promtail + Grafana deployment

```commandline
wget https://raw.githubusercontent.com/grafana/loki/v2.7.4/production/docker-compose.yaml -O docker-compose.yaml
sudo docker-compose -f docker-compose.yaml up
```

# For image logging

```commandline
grafana-cli plugins install volkovlabs-image-panel
```