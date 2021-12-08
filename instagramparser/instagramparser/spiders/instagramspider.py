import scrapy
from scrapy.http.response.html import HtmlResponse
import json
import environs
import re


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
        csrf = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.link_authenticated,
            method='POST',
            callback=self.authenticated,
            formdata={
                'username': self.LOGIN,
                'enc_password': self.PWD_HASH
            },
            headers={'X-CSRFToken': csrf}
        )

    def authenticated(self, response: HtmlResponse):
        print()

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')