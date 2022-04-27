import os
import scrapy
import yaml
from scrapy_splash import SplashRequest
from bs4 import BeautifulSoup
from ..items import CrawlingItem


SPLASH_SCRIPT = """
function main(splash, args)
  assert(splash:go(args.url))
  assert(splash:wait({}))
  return {{
    html = splash:html(),
  }}
end
"""

class RSCSpider(scrapy.Spider):
    name = "RSC"

    with open(os.path.join(os.path.dirname(__file__), 'start_urls.yaml'), 'r') as yf:
        url_yaml = yaml.safe_load(yf)

    start_urls = url_yaml[name]

    common_info = {"Publisher": name}

    exclude_article_types = ["Cover", "Front/Back Matter"]

    def start_requests(self):
        for url in self.start_urls:
            url = str(url)
            response = SplashRequest(url, self.parse, args={'lua_source': SPLASH_SCRIPT.format(0.5)}, endpoint='execute')
            yield response

    def parse(self, response):
        crawl_results = self.common_info.copy()
        issue_year = self._parse_issue_year(response)
        crawl_results.update(issue_year)
        if issue_year['Published_Year'] >= 2000:
            print("Scraping journal {}, year {}, issue {}".format(issue_year['Journal'],
                                                                  issue_year['Published_Year'],
                                                                  issue_year['Issue']))
            # Crawling
            for article_tab in response.css('div.capsule.capsule--article'):
                article_type = BeautifulSoup(article_tab.css('span.capsule__context').extract_first(),
                                             'html.parser').get_text().strip()
                open_access = bool(article_tab.css("span.capsule__context > img").extract_first())
                if article_type not in self.exclude_article_types:
                    article_page = article_tab.css('a.capsule__action::attr(href)').extract_first()
                    article_page = response.urljoin(article_page)
                    current_crawl_results = crawl_results.copy()
                    current_crawl_results.update({"Article_Type": article_type, "Open_Access": open_access})
                    request = SplashRequest(article_page, self._parse_article, args={'lua_source': SPLASH_SCRIPT.format(4)}, endpoint='execute')
                    request.meta['meta_info'] = current_crawl_results
                    yield request

            # Only crawl papers after 2000
            # previous_issue = response.css('.article-nav__bar a:nth-child(1)::attr(href)').extract_first()
            # if previous_issue:
            #     previous_issue = response.urljoin(previous_issue)
            #     yield SplashRequest(previous_issue, self.parse, args={'lua_source': SPLASH_SCRIPT.format(8)}, endpoint='execute')

    @staticmethod
    def _parse_issue_year(response):
        journal = BeautifulSoup(response.css('.page-head__vcenter span:nth-child(1)').extract_first(),
                                'html.parser').get_text().strip()
        issue_year_info = response.css('#tabissues .h--heading4').extract_first()
        year = int(issue_year_info.split(",")[0][-4:])
        issue = int(issue_year_info.split(",")[1][-2:])
        return {"Published_Year": year, "Issue": issue, 'Journal': journal}

    @staticmethod
    def _parse_article(response):
        try:
            title = BeautifulSoup(response.css("div.article__title > h2.capsule__title").extract_first(),
                                    'html.parser').get_text().strip()
            abstract = BeautifulSoup(response.css("div.capsule__text").extract_first(), 'html.parser').get_text().strip()
            doi = BeautifulSoup(response.css('.text--small').extract_first(), 'html.parser').get_text().strip()
            article_html_link = response.css("a.btn-icon--download+.btn--stack::attr(href)").extract_first()
            article_html_link = response.urljoin(article_html_link)
            article_pdf_link = response.css("a.btn-icon--download::attr(href)").extract_first()
            article_pdf_link = response.urljoin(article_pdf_link)
            authors = []
            for author in response.css('.input__label').extract():
                authors.append(BeautifulSoup(author, 'html.parser').get_text().strip())
            results = {"Title": title,
                        "Abstract": abstract,
                        "DOI": doi,
                        "Article_HTML_Link": article_html_link,
                        "Article_PDF_Link": article_pdf_link,
                        "Authors": authors
                        }
            meta_data = response.meta['meta_info']
            results.update(meta_data)
            #print(results)
            yield results
        except:
            pass