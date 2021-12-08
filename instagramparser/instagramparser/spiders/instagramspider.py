import scrapy
from scrapy.http.response.html import HtmlResponse
import json
import environs

env = environs.Env()
env.read_env('.env')


class InstagramspiderSpider(scrapy.Spider):
    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    link_authenticated = 'https://www.instagram.com/accounts/login/ajax/'
    LOGIN = env('LOGIN')
    PWD_HASH = env('PWD_HASH')

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.link_authenticated,
            method='POST',
            callback=self.authenticated,
            formdata={
                'username': self.LOGIN,
                'enc_password': self.PWD_HASH
            }
        )

    def authenticated(self, response: HtmlResponse):
        print()