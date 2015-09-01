import Token
import facebook

class FacebookCrawler:
    def __init__(self):
        self.graph = facebook.GraphAPI(Token.access_token)
        
    def get_mutual_friends_relations(self):
        friends = self.get_friends_list()
        mutual_friends = {}
        for friend in friends:
            mutual_friends[friend["id"]]=self.get_mutual_friends(friend["id"])
        return mutual_friends
        
    def get_mutual_friends(self, id):
        return self.graph.get_connections(id, "mutualfriends")['data']
        
    def get_friend_likes(self, id):
        return self.graph.get_connections(id, "likes")["data"]
        
    def get_friends_likes(self):
        friends = self.get_friends_list()
        friends_likes = {}
        for friend in friends:
            likes = self.get_friend_likes(friend["id"])
            friends_likes[friend["id"]]= likes
        return friends_likes
        
    def get_friends_list(self):
        return self.graph.get_connections("me", "friends")["data"]
    
    def get_friendlists(self):
        friendlists = self.graph.get_connections("me", "friendlists")["data"]
        friendlists_complete=[]
        
        for flist in friendlists:
            idlist=self.graph.get_connections(flist["id"], "members")["data"]
            idlist = [x["id"] for x in idlist]
            friendlists_complete.append((flist, idlist))
        return friendlists_complete
        
    def get_friends_data(self, limit=5000):
        friends = self.get_friends_list()
        count =0
        for friend in friends:
            if count < limit:
                print self.graph.get_object(friend["id"])
            count+=1
    
    def get_friends_profiles(self):
        profiles = {}
        friends = self.get_friends_list()
        for friend in friends:
            profiles[friend["id"]] = self.graph.get_object(friend["id"])
        return profiles
    
    def collect_profile_fields_names(self):
        p_set = {}
        friends = self.get_friends_list()
        for friend in friends:
            profile= self.graph.get_object(friend["id"])
            for element in profile:
                p_set[element]=profile[element]
        return p_set
    
    def get_data(self):
        #, self.get_friends_likes() # removed; saved in file
        return (self.get_friends_list(),self.get_mutual_friends_relations(),self.get_friends_profiles(), self.get_friendlists())
        
    def print_friends_attribute(self, attribute):
        friends = self.get_friends_list()
        for friend in friends:
            friend_profile = self.graph.get_object(friend["id"])
            print friend_profile.get(attribute, 'not found')
            
    # working version, uses version 1.0 access tokens
    def save_friends_likes(self):
        friends = self.graph.get_connections("me", "friends")['data']
        likes = { friend['id'] : (self.graph.get_object(str(friend['id'])+"?fields=likes")) for friend in friends }
        import json
        with open('C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\likes.json', 'w') as outfile:
            json.dump(likes, outfile)
    
    def save_friends_profiles(self):
        friends = self.graph.get_connections("me", "friends")['data']
        profiles = { friend['id'] : (self.graph.get_object(str(friend['id'])))for friend in friends }
        import json
        with open('C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\profiles.json', 'w') as outfile:
            json.dump(profiles, outfile)
            
    def save_friendlists(self):
        friendlists = self.get_friendlists()
        import json
        with open('C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\friendlists.json', 'w') as outfile:
            json.dump(friendlists, outfile)
        
def main():
    crawler = FacebookCrawler()
    #crawler.save_friends_profiles()
    #crawler.save_friends_likes()
    crawler.save_friendlists()
        
if __name__ == "__main__":
    main()