import requests
from flask import Flask, render_template, session, redirect, request, url_for, g
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
from user import User
from database import Database


app = Flask(__name__)
app.secret_key = '1234'

Database.initialise(user='postgres', database='learning', password='password', host='localhost') #kwargs that are parametrised

@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.load_to_db_by_screen_name(session['screen_name']) # declaring a g.<variable> is globbaly available during the entire request


@app.route('/')  # endpoint http://127.0.0.1:4995/
def homepage():
    return render_template('home.html')

# create a new route to allow users to connect with twitter
@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session: #if screen name is in session redirect them to the user profile
       return redirect(url_for('profile'))
    request_token = get_request_token()
    session['request_token'] = request_token

    return redirect(get_oauth_verifier_url(request_token))

@app.route('/logout')
def logout():
    session.clear() # clears user's session
    return redirect(url_for('homepage')) # redirects user back to homepage

# re-direct user to Twitter to confirm authorization
@app.route('/auth/twitter') # http://127.0.0.1:4995/login/twitter?oauth_verifier=123456
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.load_to_db_by_screen_name(access_token['screen_name'])

    if not user:
        user = User(access_token['screen_name'], access_token['oauth_token'],
                    access_token['oauth_token_secret'], None)
        user.save_to_db()

    session['screen_name'] = user.screen_name

    return redirect(url_for('profile')) # redirect user with the profile method.

@app.route('/profile') #create route for profile page
def profile():
    return render_template('profile.html', screen_name = g.user)


@app.route('/search') # route for search
def search():
    query = request.args.get('q')
    tweets = g.user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.format(query))

    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:

        r = requests.post('http://text-processing.com/api/sentiment/', data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label

    return render_template('search.html', content = tweet_texts)

app.run(port=4995, debug=True)