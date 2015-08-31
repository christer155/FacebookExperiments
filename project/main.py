# @author Hélain Schoonjans

import facebook3 as fb 
# the content of this repository: https://github.com/tuanchauict/facebook-sdk-python3
# that have been added to the site-packages folder of anaconda


oauth_access_token = open('../ressources/accessToken.txt').read()



graph = fb.GraphAPI(oauth_access_token)
profile = graph.get_object("me")
friends = graph.get_connections("me", "friends")

print(friends)
#graph.put_object("me", "feed", message="I am writing on my wall!")

