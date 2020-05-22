from database import CursorFromConnectionPool
import oauth2
from twitter_utils import consumer
import json

class User:
    def __init__(self, screen_name, oauth_token, oauth_token_secret, id):
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret
        self.id = id

    def __repr__(self):  # repr method allows to print the object
        return "<User {}>".format(self.screen_name)

    def save_to_db(self):
        # using 'with' tells psycopg2 to connect, commit and close connection.
        # no need to use commit() and close() cursors anymore
        with CursorFromConnectionPool() as cursor:
            cursor.execute('INSERT INTO users (screen_name, oauth_token, oauth_token_secret) VALUES ( %s, %s, %s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))

    # connection_pool.putconn(connection) # puts connection back to the pool

    # connection.commit() # commit writes the data to the database.
    # connection.close() # closes the connection

    @classmethod  # doesnt access the self bound method
    def load_to_db_by_screen_name(cls, screen_name):  # cls is the currently bound class a.k.a 'User' in this case.
        with CursorFromConnectionPool() as cursor:
            cursor.execute('SELECT * FROM users WHERE screen_name=%s',
                           (screen_name,))  # put comma at the end of inside bracked to tell python it is a tuple
            user_data = cursor.fetchone()  # fetchone fetches the first row of the cursor. fetchall fetches all rows
            if user_data:
                return cls(screen_name=user_data[1],
                           oauth_token=user_data[2],
                           oauth_token_secret=user_data[3],
                           id=user_data[0])


    def twitter_request(self, uri, verb = 'GET'):
        # Create an 'authorised_token'Token object and use that to perform Twitter API calls on behalf of the user
        authorised_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorised_client = oauth2.Client(consumer, authorised_token)

        # Make Twitter API Calls
        response, content = authorised_client.request(uri, verb)
        if response.status != 200:
            print("An error occured when searching!")

        return json.loads(content.decode('utf-8'))



        # connection_pool.putconn(connection) # puts connection back to the pool
