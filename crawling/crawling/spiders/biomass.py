import scrapy
from ..items import CrawlingItem

class BiomassSpider(scrapy.Spider):
    name = "biomass"
    start_urls = [
        'http://biomassmagazine.com/newsletter/biomass-week/'
    ]

    def parse(self, response):
        elements = response.css('#colLeft a')
        #for element in elements:
        for i in range(0, 10):
            element = elements[i]
            week = element.css('::text').extract_first()
            url = element.css('::attr(href)').extract_first()
            # Items
            if week and url:
                yield response.follow(url, callback = self.parseWeek, 
                    meta = {'week_index':i, 'week':week, 'url':url })

    def parseWeek(self, response):
        # Articles
        elements = response.css('#articles div')
        articles = 0
        for index, element in enumerate(elements):
            article = {}
            article['week_index'] = response.meta['week_index']
            article['article_index'] = index
            article['title'] = element.css('h3::text').extract_first()
            article['description'] = element.css('span::text').extract_first()
            article['url'] = element.css('br+ a::attr(href)').extract_first()
            articles = articles + 1
            yield response.follow(article['url'], callback = self.parseArticle, 
                meta = {
                    'article_index':index,
                    'article':article
                })
        # Yield item
        item = CrawlingItem()
        item['week_index'] = response.meta['week_index']
        item['week'] = response.meta['week']
        item['url'] = response.meta['url']
        item['articles'] = articles
        yield item

    def parseArticle(self, response):
        article = response.meta['article']
        # Elements
        elements = response.css('.post')
        article['author'] = elements.css('.author .author a::text').extract_first()
        article['text'] = ''.join(elements.css('p::text').extract())
        yield article