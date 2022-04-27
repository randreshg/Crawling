# WEB CRAWLING TO  biofuelsdigest.com


## Command:
Start splash server
```
sudo docker run -it -p 8050:8050 --rm scrapinghub/splash
```

Call spider
```
cd crawling
scrapy crawl biomass
```

Output file
```
crawling/output/articles.json
crawling/output/content.json
```