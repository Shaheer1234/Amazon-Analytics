import scrapy
import urllib
from amazon.items import AmazonItem
import os


class amazonSpider(scrapy.Spider):
    imgcount = 1
    name = "amazon"
    allowed_domains = ["amazon.com"]
    
    def start_requests(self):
        # start path for books : http://www.amazon.com/s/ref=sr_st_review-count-rank?keywords=book&rh=n%3A283155%2Ck%3Abook&qid=1459287325&sort=review-count-rank
        yield scrapy.Request("http://www.amazon.com/s/ref=sr_pg_1?page=1&keywords=Books",self.parse)
        
        for i in range(2,50):
            #path for books: ttp://www.amazon.com/gp/search/ref=sr_pg_"+str(i)+"?rh=n%3A283155%2Ck%3Abook&page="+str(i)+"&sort=review-count-rank&keywords=book"
            yield scrapy.Request("http://www.amazon.com/s/ref=sr_pg_"+str(i)+"?page="+str(i)+"&keywords=Books",self.parse)
    
    
    def parse(self,response):
        
        namelist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@title').extract()
        htmllist = response.xpath('//a[@class="a-link-normal s-access-detail-page  a-text-normal"]/@href').extract()
        #data asin class for Books: s-result-item celwidget
        asInlist = response.xpath('//li[@class="s-result-item celwidget"]/@data-asin').extract()
        #data asin class for Electronics s-result-item s-result-card-for-container  a-declarative celwidget
        #imglist = response.xpath('//img[@class="s-access-image cfMarker"]/@src').extract()
        listlength = len(namelist)
        pricelist = response.xpath('//span[@class="a-size-base a-color-price s-price a-text-bold"]/text()').extract()
        print len(pricelist)
        
        
        for i in range(0,listlength):
            yield scrapy.Request("http://www.amazon.com/product-reviews/"+asInlist[i],self.parse_reviews)
            item = AmazonItem()
            item['Pid'] = asInlist[i]
            item['Name'] = namelist[i]
            item['Path'] = htmllist[i]
            item['Price'] = pricelist[i] 
            item['Rid'] = ''
            yield item
            
    def parse_reviews(self,response):
        response = response.replace(body=response.body.replace('<br />', '\n'))
        #reviewlist =  response.xpath('//span[@class="a-size-base review-text"]/text()').extract()
        reviewlist = []
        reviewidlist = response.xpath('//div[@class="a-section review"]/@id').extract()
        reviewer = response.xpath('//a[@class="a-size-base a-link-normal author"]/text()').extract()
        for id in reviewidlist:
            reviewlist.append(response.xpath('//div[@id="'+id+'"]/div/span[@class="a-size-base review-text"]/text()').extract()[0])
        n_reviews =  len(reviewlist)
        print "review id", len(reviewidlist)
        print "reviewers",len(reviewer)
        
        for i in range(0,n_reviews):
            item = AmazonItem()
            item['Pid'] = response.url.split('/')[-1]
            item['Rid'] = reviewidlist[i]
            item['Rname'] = reviewer[i]
            item['Review'] = reviewlist[i]
            yield item
