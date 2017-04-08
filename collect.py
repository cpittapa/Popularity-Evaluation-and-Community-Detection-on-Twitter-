import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from tweepy import Stream
import time
import os

'''
Tokens for twitter
'''
consumer_key = 'egCRs7HwOpUSCnVgsuTe9YwkL'
consumer_secret = 'KXGhI5ItesY9q818Vuk699IfbLeJ4VUoBKlr5iG8mxyG0pJtXn'
access_token = '803843026569330693-AJ90q3bih6qk7Xd0c0Vwf6GmeqzRdCj'
access_token_secret = '2C8jZFSurPnbqwXYCUdhFqWQsID75iEQPaMn4CsjPIF0L'


'''
SETTINGS

Please note change of each setting will reult in different in time required for data collection. By default setting,
this script will collect new tweets for classification.

'''
friend_collection=False  #This is for friends collection
tweet_collection_test=True   #This is for tweet collection
#Please change the counts below if more tweets or friends needs to collected
no_of_tweets=40
friends_count=20

user_id="@selenagomez" #user id of the celebrity
search_query="selena gomez" #twitter term to track


ids=[]
number_of_tweets=0


'''
Filename created based on track term
'''
def filename(fname):
    return ''.join((x) for x in fname)

'''
TO handle rate limits in twitter
'''
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)


'''
StreamListener class has functions to write the tweets into a file
'''
class listener(StreamListener):

    def __init__(self, data_dir, query):
        query_fname = filename(query.replace(" ", ""))
        self.outfile = "%s/Test_%s.txt" % (data_dir, query_fname)
        try:
            os.remove(self.outfile)
        except OSError:
            pass

    def on_data(self, data):
        global number_of_tweets
        while (number_of_tweets < no_of_tweets):
            number_of_tweets += 1
            with open(self.outfile, 'a') as f:
                f.write(str(data))
                print(data)
                return True
            f.close()
        return False


'''
Function to collect friends of a user id given
'''
def get_friends(user_id):
    pagecount = 0
    for page in limit_handled(tweepy.Cursor(api.friends_ids, id=user_id).pages()):
        ids = []
        ids.extend(page)
        filename = "data/friends/%s.txt" % user_id
        a = open(filename, "w")
        json.dump(ids, a)
        a.close()
        print("Number of friends collected :", len(ids))
        pagecount += 1
        break

'''
Function to collect friends of friends stored in the file .i.e friends of the celebrity
'''
def get_friends_of_friends():
    i=0
    file1 = open('data/friends.txt', 'r')
    file = file1.read()
    data = json.loads(file)
    collected=[]
    for friend in list(data):
        if(friend not in collected):
            print("Friend %d: %d"%(i,friend))
            collected.append(friend)
            get_friends(friend)
            i+=1

'''
Collects a subset of friends in twitter of that celebrity
'''
def get_frineds_main(user_id):
    pagecount=0
    filename = "data/friends.txt"
    try:
        os.remove(filename)
    except OSError:
        pass
    for page in limit_handled(tweepy.Cursor(api.friends_ids, screen_name=user_id,count=friends_count).pages()):
        ids=[]
        ids.extend(page)
        a = open(filename, "w")
        json.dump(ids, a)
        a.close()
        print ("Number of friends collected for %s are %d  " %(user_id,len(ids)))
        pagecount+=1
        break



'''
Main Method
'''
if __name__ == '__main__':

    #Create the tweepy api object
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)


    #Collecting tweets
    if (tweet_collection_test == True):
        twitter_stream = Stream(auth, listener("data", search_query))
        twitter_stream.filter(languages=["en"],track=[search_query])
        print("Tweet collection Done")

    '''
    Data Collection for Community detection. Set as True at top to collect again.
    If not, already collected data stored in file in data folder will be used.

    If decided to run friend_collection again, please not there is a wait time depending of the friends_count set on top
    '''
    if(friend_collection==True):
        get_frineds_main(user_id)
        get_friends_of_friends()
        print("Friends collection Done")