import facebookcrawler as fc
import socialgraph as sg

def main():
    crawler = fc.FacebookCrawler()
    graph = sg.SocialGraph()
    
    #needs to use the API version 1.0 for the profiles and likes
    crawler.save_friends_profiles()
    crawler.save_friends_likes()
    crawler.save_friendlists()
    
    
    graph.add_friends_data(crawler.get_data())
    graph.save_to_jsonfile("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\Code\\my_network.json")
        
if __name__ == "__main__":
    main()