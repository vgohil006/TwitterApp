import oauth2
import constants
import urllib.parse as urlparse


consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)

def get_request_token():
    # Create a Consumer which uses a CONSUMER_KEY and CONSUMER_SECRET to identify our app
    client = oauth2.Client(consumer)

    # Use the client to perform a request for the request_token
    response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')  # pass rhe request token url and what sort of request it is - POST
    if response.status != 200:
        print("An error occured getting the request token from Twitter!")

    # Get the request_token passing the query string
    return dict(urlparse.parse_qsl(
        content.decode('utf-8')))  # parses a query string, convert the query string into a dictionary

def get_oauth_verifier(request_token):
    # Ask user to authorize the app and get a pin code
    print("Go to the following website in your browser:")
    print(get_oauth_verifier_url(request_token))

    return input("What is the PIN? ")

def get_oauth_verifier_url(request_token):
    return "{}?oauth_token={}".format(constants.AUTHORISATION_URL, request_token['oauth_token'])

def get_access_token(request_token, oauth_verifier):
    # Create a token object which contains the request token and the verifier
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)

    # Create a client with consumer, app and newly created and verified token
    client = oauth2.Client(consumer, token)

    # Ask Twitter for an access token. Twitter knows the user because it has verified the request token
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    return  dict(urlparse.parse_qsl(content.decode('utf-8')))





