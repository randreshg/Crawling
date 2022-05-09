# WEB CRAWLING TO  biofuelsdigest.com


## Command:
Start splash server
```
sudo docker pull scrapinghub/splash
sudo docker run -it -p 8050:8050 --rm scrapinghub/splash
```

Start elastic search server 
```
sudo systemctl start elasticsearch
```

Call spider
```
cd crawling
scrapy crawl RSC
```

Output file
```
crawling/output/articles.json
crawling/output/content.json
```