# @author Hélain Schoonjans

import facebook3 as fb
import sys 
# the content of this repository: https://github.com/tuanchauict/facebook-sdk-python3
# that have been added to the site-packages folder of anaconda


# add error message in case of missing file or bad token!
oauth_access_token = open('../ressources/accessToken.txt').read()



graph = fb.GraphAPI(oauth_access_token)

friends = {}

try:
    some_friends = graph.get_connections("me", "friends")
    print(some_friends)
except:
    print("Unexpected error:",  sys.exc_info()[0])


#print(graph.fetch_url(some_friends['paging']['next']))

#print(graph.get_connections("me", some_friends['data'][0]["id"]))



# now i need a method to fill the friends dictionary
    # get the sex
    # get the likes


# another to save the dictionary



#profile = graph.get_object("me")
#graph.put_object("me", "feed", message="I am writing on my wall!")

