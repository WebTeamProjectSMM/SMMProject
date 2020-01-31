import os
from flask import Flask, render_template, url_for, redirect, \
				  flash, send_from_directory, request, session, jsonify

from flask_login import LoginManager, UserMixin, login_user, \
						logout_user, current_user

from rauth import OAuth1Service

from authentication import OAuthLogin

app = Flask(__name__, template_folder='public')

app.config['SECRET_KEY'] = 'dumbkey'
app.config['OAUTH_CREDENTIALS'] = {
	'twitter':{
		# put your api key here
		'id': '',
		# put api secret key here							
		'secret': ''			
	}
}

login_manager = LoginManager(app)
login_manager.login_view = 'index'

# here in case we need it
username = None

# GET statuses/home_timeline.json
@app.route('/api/<provider>/posts', methods=['GET'])
def get_timeline(provider):
	oauth = OAuthLogin.get_provider(provider)
	return jsonify(oauth.get_tweets(10))

# AUTHENTICATION
@app.route('/api/twitter')
def twitter_auth():
	return redirect(url_for('oauth_authorize', provider='twitter'))

# not implemented in authentication.py
@app.route('/api/facebook')
def facebook_auth():
	return redirect(url_for('oauth_authorize', provider='facebook'))

# not implemented in authentication.py
@app.route('/api/instagram')
def instagram_auth():
	return redirect(url_for('oauth_authorize', provider='instagram'))

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('test'))
	oauth = OAuthLogin.get_provider(provider)
	return oauth.authorize()

@app.route('/callback/<provider>')
def oauth_callback(provider):
	if not current_user.is_anonymous:
		return redirect(url_for('test'))
	oauth = OAuthLogin.get_provider(provider)
	social_id, username = oauth.callback()

	if social_id is None:
		flash('Something went wrong with Authentication')
		return redirect(url_for('index'))
	return redirect(url_for('get_timeline', provider=provider))

# catch all, must be after API calls, not sure if this works,
# we'll find out later lmao
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
	path_dir = os.path.abspath("client/public")
	if path != "" and os.path.exists(os.path.join(path_dir, path)):
		print('Path', os.path.join(path_dir), path)
		return send_from_directory(os.path.join(path_dir), path)
	else:
		return send_from_directory(os.path.join(path_dir), 'index.html')

if __name__ == "__main__":
	app.run(debug=True, port=8080)