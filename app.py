import os
from flask import Flask,redirect, url_for
from flask_dance.contrib.github import make_github_blueprint, github
from flask_dance.contrib.twitter import make_twitter_blueprint , twitter




app = Flask(__name__)

app.config['SECRET_KEY'] = 'dumbkey'
app.config['OAUTH_CREDENTIALS'] = {
	'twitter':{
		# put your api key here
		'id': '',
		# put api secret key here							
		'secret': ''			
	}
}
github_blueprint = make_github_blueprint(
    client_id="139648bfd126633a1997",
    client_secret="2eb5c5fd9e36c65f46dfc8e01a9967a024e35c62",
)

twiter_blueprint = make_twitter_blueprint(
	api_key = "rWKhw4FaMIZzUiZrKKqbrFDnF",
	api_secret = "aOoD9XZ80M2tqBvcZpmLyBLyHIF3dMiNbOb6pHusY31pZjFCl5",
)

app.register_blueprint(github_blueprint, url_prefix="/login")
app.register_blueprint(twiter_blueprint, url_prefix="/twitter_login")

@app.route("/github")
def github_login(): 
	if not github.authorized: 
		return redirect(url_for("github.login"))
	resp = github.get('/user')
	assert resp.ok
	return "You are @{login} on GitHub".format(login=resp.json()["login"])

@app.route("/twitter")
def twitter_login():
	if not twitter.authorized:
		return redirect(url_for("twitter.login"))


# here in case we need it
username = None

#start flask app 
if __name__ == "__main__":
	app.run(debug=True, port=8080)