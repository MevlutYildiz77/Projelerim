import scrapy
from scrapy.crawler import CrawlerProcess
import win32com.client as win32
import os



class GPUSpider(scrapy.Spider):
    name = "GPU"
  
    def start_requests(self):
        # go to the best buy website
        url = "https://www.bestbuy.com/site/searchpage.jsp?st=gpu"
        
        # Set the headers here because best buy disable random requests, we sending the request acting as Firefox
        headers = {'User-agent': 'Opera/94.0.0.0',"Accept-Encoding": "*",
        "Connection": "keep-alive"}                   # Mozilla/5.0

        # Sending the request
        yield scrapy.http.Request(url, headers=headers)

    def parse(self, response):
        # get html element has the class of sku_item
        for gpu in response.css('li.sku-item'):
            yield {
                'product_title': gpu.css('div.sku-title a::text').get(), # select div tag with css name of sku-title
                'product_price': gpu.css('div.priceView-customer-price span::text').get(), # select div tag with css name of customer-price
                'availability': gpu.xpath("//button[contains(@class, 'add-to-cart-button')]/@data-button-state").get() # select data-button-state attibute of add-to-cart-button
            }
        # click on the next page button
        next_page = response.css('a.sku-list-page-next').attrib['href']
        # This is a recursive function to parse next page until there is no next page
        if next_page is not None:
            headers = {'User-agent': 'Opera/94.0.0.0',"Accept-Encoding": "*",
            "Connection": "keep-alive"}    #Mozilla/5.0
            yield response.follow(next_page, callback=self.parse, headers = headers)



if __name__ == "__main__":
    print("Program started... ")
    # set the output file as csv
    setting = {
        "FEEDS": {
            "gpu.csv": {"format": "csv"},
        }
    }
    # start the crawler 
    process = CrawlerProcess(settings = setting)
    process.crawl(GPUSpider)
    process.start()
    # Use excel to open gpu.csv (the file we just output it )
    wb_path = "gpu.csv"
    if os.path.exists(wb_path):
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.Workbooks.Open(os.path.abspath(wb_path), ReadOnly=1)
        excel.Visible = 1
        excel.WindowState = win32.constants.xlMaximized
    print("Program finished"




if os.path.exists(wb_path):
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Workbooks.Open(os.path.abspath(wb_path), ReadOnly=1)
excel.Visible = 1
excel.WindowState = win32.constants.xlMaximized

