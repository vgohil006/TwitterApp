from user import User
from database import Database
from twitter_utils import get_request_token, get_oauth_verifier, get_access_token


Database.initialise(user='postgres', database='learning', password='password', host='localhost') #kwargs that are parametrised

# Request User's email and check whether email exists in the database
user_email = input("Enter your email address: ")
user = User.load_to_db_by_email(user_email)

if not user:

    # Get the request_token passing the query string
    request_token = get_request_token() #parses a query string, convert the query string into a dictionary

    oauth_verifier = get_oauth_verifier(request_token)

    access_token = get_access_token(request_token, oauth_verifier)

    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name:")


    user = User(user_email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'], None)
    user.save_to_db()

tweets = user.twitter_request('https://api.twitter.com/1.1/search/tweets.json?q=computer+filter:images')
for tweet in tweets['statuses']:
    print(tweet['text'])

