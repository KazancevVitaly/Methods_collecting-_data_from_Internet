import scrapy
from scrapy.http.response.html import HtmlResponse
import json
import environs
import re
from urllib.parse import urlencode
from instagramparser.items import InstagramparserItem

env = environs.Env()
env.read_env('.env')


class InstagramspiderSpider(scrapy.Spider):
    name = 'instagramspider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    link_authenticated = 'https://www.instagram.com/accounts/login/ajax/'
    LOGIN = env('LOGIN')
    PWD_HASH = env('PWD_HASH')
    users = [
        'codeclasskazan',
        'veralutik25'
    ]
    friendships_link = 'https://i.instagram.com/api/v1/friendships/'
    followers = 'followers/?'
    following = 'following/?'

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
        json_data = response.json()
        if json_data.get('authenticated'):
            for user in self.users:
                yield response.follow(
                    f'/{user}',
                    callback=self.user_parse,
                    cb_kwargs={'username': user}
                )

    def user_parse(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        subscribers_link = f'{self.friendships_link}{user_id}/{self.followers}count=12&search_surface=follow_list_page'
        yield response.follow(
            subscribers_link,
            callback=self.subscribers_parse,
            cb_kwargs={
                'username': username,
                'user_id': user_id
            }
        )

    def subscribers_parse(self, response: HtmlResponse, username, user_id):
        subscribers_info = json.loads(response.text)
        try:
            max_id = subscribers_info['next_max_id']
        except KeyError:
            max_id = False
        if max_id:
            next_page = f'{self.friendships_link}{user_id}/{self.followers}count=12&max_id={max_id}&search_surface=follow_list_page'
            yield response.follow(
                next_page,
                callback=self.subscribers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id
                }
            )
        subscribers = subscribers_info.get('users')
        for subscriber in subscribers:
            item = InstagramparserItem(
                user_id=user_id,
                username=username,
                subscriber_id=subscriber['pk'],
                subscriber_link=f'{self.start_urls[0]}{subscriber["username"]}',
                subscriber_name=subscriber['full_name'],
                subscriber_login=subscriber['username'],
                subscriber_avatar_link=subscriber['profile_pic_url'],
                subscriber_on=False    # False если подписчик нашего usera и True если наш user подписан на него
            )
            yield item
        if not max_id:
            users_subscribers_link = f'{self.friendships_link}{user_id}/{self.following}count=12'
            yield response.follow(
                users_subscribers_link,
                callback=self.users_subscribers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id
                }
            )

    def users_subscribers_parse(self, response: HtmlResponse, username, user_id):
        print()
        subscribers_info = json.loads(response.text)
        try:
            max_id = subscribers_info['next_max_id']
        except KeyError:
            max_id = False
        if max_id:
            next_page = f'{self.friendships_link}{user_id}/{self.following}count=12&max_id={max_id}'
            yield response.follow(
                next_page,
                callback=self.users_subscribers_parse,
                cb_kwargs={
                    'username': username,
                    'user_id': user_id
                }
            )
        subscribers = subscribers_info.get('users')
        for subscriber in subscribers:
            item = InstagramparserItem(
                user_id=user_id,
                username=username,
                subscriber_id=subscriber['pk'],
                subscriber_link=f'{self.start_urls[0]}{subscriber["username"]}',
                subscriber_name=subscriber['full_name'],
                subscriber_login=subscriber['username'],
                subscriber_avatar_link=subscriber['profile_pic_url'],
                subscriber_on=True
            )
            yield item

    def fetch_csrf_token(self, text):
        ''' Get csrf-token for auth '''
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')