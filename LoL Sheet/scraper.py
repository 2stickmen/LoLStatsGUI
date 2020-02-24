from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from bs4 import BeautifulSoup
import os

golgg = 'https://gol.gg/champion/champion-stats/{}/season-S10/split-Spring/tournament-ALL/patch-ALL/role-ALL/league-1/'

class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [golgg.format(i) for i in range(149)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-8]
        filename = '-%s.html' % page
        with open(os.getcwd() + '\\scraped\\' + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        
configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(QuotesSpider)
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished\


with open('thresh.html') as fp:
    soup = BeautifulSoup(fp,"lxml")
