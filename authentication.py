import json

from rauth import OAuth1Service, OAuth2Service
from flask import request, url_for, current_app, redirect, session

class OAuthLogin(object):
    providers = None
    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        # http://127.0.0.1:8080/callback/twitter
        return url_for('oauth_callback', provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers == None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        # returns twitter authentication object
        return self.providers[provider_name]


class TwitterLogin(OAuthLogin):
    def __init__(self):
        super(TwitterLogin, self).__init__('twitter')
        self.service = OAuth1Service(
            name='twitter',
            consumer_key=self.consumer_id,
            consumer_secret=self.consumer_secret,
            request_token_url='https://api.twitter.com/oauth/request_token',
            authorize_url='https://api.twitter.com/oauth/authorize',
            access_token_url='https://api.twitter.com/oauth/access_token',
            base_url='https://api.twitter.com/1.1/'
        )
        self.oauth_session = None

    def authorize(self):
        # get request token (oauth_token, oauth_token_secret) from callback url
        request_token = self.service.get_request_token(
            params={'oauth_callback': self.get_callback_url()}
        )
        # store the request token as session variable & redirect to authorization url
        session['request_token'] = request_token
        return redirect(self.service.get_authorize_url(request_token[0]))

    def callback(self):
        request_token = session.pop('request_token')
        if 'oauth_verifier' not in request.args:
            return None, None
        self.oauth_session = self.service.get_auth_session(
            request_token[0],
            request_token[1],
            data={'oauth_verifier': request.args['oauth_verifier']}
        )

        verify = self.oauth_session.get('account/verify_credentials.json').json()
        social_id = 'twitter$' + str(verify.get('id'))
        username = verify.get('screen_name')
        
        return social_id, username

    def get_tweets(self, nbr_posts):
        tweets_json = self.oauth_session.get('statuses/home_timeline.json', params ={
            'count': nbr_posts
        }).json()
        return tweets_json
