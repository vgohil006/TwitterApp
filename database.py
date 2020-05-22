from psycopg2 import pool

class Database:

    #initialise a connection pool property inside database class
    __connection_pool = None # double underscrore make the variable private and hidden from other programs

    # @staticmethod # with static method you do not have to initalize the class
    # def initialise(): # initialise method does not get executed immediately
    #     Database.connection_pool = pool.SimpleConnectionPool(1,  # min no of connections
    #                                                          10,  # max no. of connections
    #                                                          user='postgres',
    #                                                          database='learning',
    #                                                          password='password',
    #                                                          host='localhost')


    @classmethod
    def initialise(cls, **kwargs):
        cls.__connection_pool = pool.SimpleConnectionPool(1,  # min no of connections
                                                          10,  # max no. of connections
                                                          **kwargs) # **kwargs will use any number of named parameters to intialise

    @classmethod
    def get_connection(cls):
        return cls.__connection_pool.getconn()

    @classmethod
    def return_connection(cls, connection): #pass the connection as a parameter
        Database.__connection_pool.putconn(connection) #pass the conn parameter

    @classmethod
    def close_all_connections(cls):
        Database.__connection_pool.closeall()

#Create class called ConnectionPool()
class CursorFromConnectionPool(): # define a new class with connection pool and a cursor
    def __init__(self):
        self.connection = None # initialise connection object
        self.cursor = None # initialise cursor object


    def __enter__(self):
        self.connection = Database.get_connection() # define the connection
        self.cursor = self.connection.cursor() # define the cursor
        return self.cursor # gets a new connection
    # using the above class method actuall create a new connection pool every time you run the with ConnectionPool() in the query
    # This creates overhead by creating connection pools as well as connections. Inorder to stop the overhead, return the connection pack to the
    # connection pool

    def __exit__(self, exc_type, exc_val, exc_tb): # exception_type, exception_value, exception_traceback
        if exc_val is not None: # if there is an exception error then roll back connection (TypeErr, AttributeErr, ValErr etc)
            self.connection.rollback()
        else:
            self.cursor.close() # clse the cursoe
            self.connection.commit() # commit the connection
        Database.return_connection(self.connection) # close connection and return to connection pool



# defining a connection method to the database that you can use. This will connect, commit and close the connection.
#def connect():
 #   return psycopg2.connect (user='postgres', database='learning', password='password', host='localhost')