# @author Hélain Schoonjans

import api.facebook as fb
import sys 

# add error message in case of missing file or bad token!
oauth_access_token = open('../ressources/accessToken.txt').read()



graph = fb.GraphAPI(oauth_access_token)

friends = {}

try:
    some_friends = graph.get_connections("me", "friends")
    print(some_friends)
    next_page=graph.fetch_url(some_friends['paging']['next'])
    print(next_page)
    # sadly facebook doesn't allow anymore to get the app user's friends' 
    # information. This makes all of this pretty useless.
    # Solution: build a real crawler !
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

