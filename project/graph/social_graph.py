# -*- coding: utf-8 -*-
import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph

class SocialGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.friendlists=None
        
    def generate_test_graph(self):
        for i in range(13):
            self.G.add_node(i, name='test node', gender='unknown', likes={})
        for i in range(4):
            for j in range(i+1, 4):
                if j==i:
                    continue
                self.G.add_edge(i, j)
        for i in range(5, 9):
            for j in range(i+1, 9):
                if j==i:
                    continue
                self.G.add_edge(i, j)
        for i in range(9, 13):
            for j in range(i+1, 13):
                if j==i:
                    continue
                self.G.add_edge(i, j)
        self.G.add_edge(3, 4)
        self.G.add_edge(4, 5)
        
    def draw(self):
        nx.draw(self.G)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_draw.pdf")
        
    def get_colors(self):
        return ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow']
    
    
    def draw_random_communities(self):
        partition = self.find_partition()[1]
        node_color=[float(partition[v]) for v in partition]
        labels = self.compute_labels()
        nx.draw_random(self.G,node_color=node_color, labels=labels)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_random.pdf")
        
    def draw_circular_communities(self):
        partition = self.find_partition()[1]
        node_color=[float(partition[v]) for v in partition]
        labels = self.compute_labels()
        nx.draw_circular(self.G,node_color=node_color, labels=labels)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_circular1.pdf")
        
    def draw_spectral_communities(self):
        partition = self.find_partition()[1]
        node_color=[float(partition[v]) for v in partition]
        labels = self.compute_labels()
        nx.draw_spectral(self.G,node_color=node_color, labels=labels)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_spectral.pdf")
        
    def draw_spring_communities(self, full_names='False', k=None, iterations=50, scale=1.0):
        partition = self.find_partition()[1]
        #colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow']
        #node_color=[colors[partition[v]] for v in partition]
        node_color=[float(partition[v])*2.0 for v in partition]
        if not(full_names):
            labels = self.compute_labels()
        else:
            labels =  {}
            for node in self.G.nodes():
                labels[node]= self.G.node[node].get('name', '')
        nx.draw_spring(self.G,node_color=node_color, labels=labels, k=k, iterations=iterations, scale=scale, cmap=plt.cm.hsv)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_spring.pdf")
        
    def draw_shell_communities(self):
        partition = self.find_partition()[1]
        node_color=[float(partition[v]) for v in partition]
        labels = self.compute_labels()
        nx.draw_shell(self.G,node_color=node_color, labels=labels)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_shell.pdf")
        
    def save_to_jsonfile(self, filename):
        g = self.G
        g_json = json_graph.node_link_data(g)
        json.dump(g_json, open(filename, 'w'))
        
    def read_json_file(self, filename):
        self.G = json_graph.node_link_graph(json.load(open(filename)))
        print("Read in file " + filename)
        
    def add_friends_data(self, data):
        self.add_friends(data[0])
        self.add_friendships(data[1])
        self.add_friend_profiles(data[2])
        self.friendlists = data[3]
        #self.add_friend_likes(data[4])
        
    def add_friend_likes(self, flikes):
        for node in self.G.nodes():
            self.G.node[node]['likes']=flikes[node]
    
    def read_likes_file(self, filename):
        # read the files
        json_data=open(filename)
        data = json.load(json_data)
        json_data.close()
        # for each person in like dict
        for id in data:
            if 'likes' in data[id]:
                # add the likes to the equivalent profile
                if 'data' in data[id]['likes']:
                    for like in data[id]['likes']['data']:
                        self.G.node[id]['likes'][like['id']]=like
                        
    
    def add_friends(self, friends):
        for friend in friends:
            self.G.add_node(friend["id"], name=friend["name"], gender="unknown", likes={})
    
    def add_friendships(self, friendships):
        for friend_id in friendships:
            for mutual_friend in friendships[friend_id]:
                self.G.add_edge(friend_id, mutual_friend["id"])
    
    def add_friend_profiles(self, profiles):
        for friend_id in profiles:
            profile_info = self.remove_useless_info(profiles[friend_id])
            self.G.node[friend_id]['gender']=profile_info['gender']
    
    def remove_useless_info(self, profile):
        profile_info={}
        profile_info['gender'] = profile.get('gender', 'unknown')
        return profile_info
    
    def compute_labels(self):
        labels ={}
        for node in self.G.nodes():
            labels[node]=self.get_initials(node)
        return labels
    
    def get_initials(self, id):
        name = self.G.node[id].get('name', '')
        initials = ""
        for word in name.split():
            initials+=word[0].upper()
        return initials

    # create the attribute vector of dictionary
    def get_attributes(self):
        # create the list of attributes
        partition = self.find_partition()[1]
        attributes = []
        attributes.append(('community', [str(res) for res in list(set([partition[v] for v in partition]))]))
        
        # create the content of each nodes line
        data = ""
        for node in self.G.nodes():
            data+=self.get_node_attributes(node)+','+str(partition[node])+'\n'
        attributes.append(('gender', ['male', 'female', 'unknown']))
        return attributes, data
    
    def get__likes(self, node):
        return self.G.node[node]['likes']
    
    def get_list_of_likes(self):
        likes={}
        for node in self.G.nodes():
            for like in self.G.node[node]['likes']:
                likes[like]=self.G.node[node]['likes'][like]
        return sorted(set([i['name'] for i in likes.values()]))
    
    def get_gender_attributes(self):
        likes=self.get_list_of_likes()
        attributes = []
        attributes.extend(self.getProfileTuples("../ressources/profiles.json"))
        
        for like in likes:
                attributes.append(('_'.join(like.split()), ['liked', 'not_liked']))
        attributes.append(('gender', ['male', 'female', 'unknown']))         
        
        return attributes
        
    def get_gender_data(self):
        likes=self.get_list_of_likes()
        information = ['relationship_status', 'locale']
        information2 = ['hometown', 'location']
        # create the content of each nodes line
        data = ""
        node_number = 0
        profiles=self.get_profiles()
        import time
        start_time = time.time()
        for node in self.G.nodes():
            data2=''
            
            #add other profile informations
            
            if node in profiles:
                
                for info in information:
                    data2+=('_'.join(profiles[node].get(info, "NA").split()))+","
                
                for info in information2:
                    data2+=('_'.join(profiles[node].get(info, {'name':"NA"})['name'].replace(',', '').split()))+","
                 
                info = 'birthday'
                test = profiles[node].get(info, "0/0/NA").split('/')
                if len(test)==3:
                    data2+=test[2]+","
                else:
                    data2+='NA'+"," 
                    
                # college and ULB
                res = profiles[node].get('education', [])
                if not(res):
                    data2+='no'  
                    data2+='no'+"," 
                else:
                    found = False
                    for edu in res:
                        if 'school' in edu:
                            #'Coll\xe8ge Saint - Michel'
                            if edu["school"]["name"]=='Collège Saint - Michel':
                                data2+="yes"+","
                                found=True
                                break
                            if edu["school"]["name"]=='Collège St-Michel':
                                data2+="yes"+","
                                found=True
                                break
                    if not(found):
                        data2+="no"+","
                    found = False
                    for edu in res:
                        if 'school' in edu:
                            #'Coll\xe8ge Saint - Michel'
                            if edu["school"]["name"]=='Université libre de Bruxelles':
                                data2+="yes"+","
                                found=True
                                break
                            """if edu["school"]["name"]=='ULB BE':
                                data2+=","+"yes"
                                found=True
                                break"""
                            if edu["school"]["name"]=='Vrije Universiteit Brussel':
                                data2+="yes"+","
                                found=True
                                break
                            if 'ULB' in edu["school"]["name"]:
                                data2+="yes"+","
                                found=True
                                break   
                    if not(found):
                        data2+="no"+","
            else:
                for info in information:
                    data2+="NA"+","
                
                for info in information2:
                    data2+="NA"+","
                    
                #birthday
                data2+="NA"+","
                
                # college and 
                data2+="no"+","
                data2+="no"+","
            
            for like in likes:
                # if the user has not liked the page
                if not(like in [i['name'] for i in self.G.node[node]['likes'].values()]):
                    data2+='not_'
                data2+='liked'
                data2+=","
                
                
            data2+=self.G.node[node].get('gender', 'unknown')
            data2+='\n'
            
            data+=data2
            print("Node ", node_number + 1, " processed in " ,time.time() - start_time, "seconds.")
            node_number+=1
        return data
        
    def get_profiles(self, filename="../ressources/profiles.json"):
        json_data=open(filename)
        profiles = json.load(json_data)
        json_data.close()
        return profiles
        
    # create the attribute vector of dictionary
    def get_attributes_with_likes(self, userList):
        not_keyword= 'not_'
        list_likes={}
        for node in self.G.nodes():
            for like in self.G.node[node]['likes']:
                list_likes[like]=self.G.node[node]['likes'][like]
        set_ = set(list_likes.keys())
        set_ = set([i['name'] for i in list_likes.values()])
        list_likes=sorted(set_)
        
        # create the list of attributes
        attributes = []
        
        
        # add other profile informations
        attributes.extend(self.getProfileTuples("../ressources/profiles.json"))
        
        for like in list_likes:
                attributes.append(('_'.join(like.split()), ['liked', not_keyword+'liked']))
        attributes.append(('gender', ['male', 'female', 'unknown'])) 
        json_data=open("../ressources/profiles.json")
        profiles = json.load(json_data)
        json_data.close()
            
        information = ['relationship_status', 'locale']
        information2 = ['hometown', 'location']
        # create the content of each nodes line
        data = ""
        node_number = 0
        import time
        start_time = time.time()
        for node in self.G.nodes():
            data2=''
            
            #add other profile informations
            
            if node in profiles:
                
                for info in information:
                    data2+=","+('_'.join(profiles[node].get(info, "NA").split()))
                
                for info in information2:
                    data2+=","+('_'.join(profiles[node].get(info, {'name':"NA"})['name'].replace(',', '').split()))
                 
                info = 'birthday'
                test =profiles[node].get(info, "0/0/NA").split('/')
                if len(test)==3:
                    data2+=","+test[2]
                else:
                    data2+=","+'NA'   
                    
                # college and ULB
                res = profiles[node].get('education', [])
                if not(res):
                    data2+=","+'no'  
                    data2+=","+'no' 
                else:
                    found = False
                    for edu in res:
                        if 'school' in edu:
                            #'Coll\xe8ge Saint - Michel'
                            if edu["school"]["name"]=='Collège Saint - Michel':
                                data2+=","+"yes"
                                found=True
                                break
                            if edu["school"]["name"]=='Collège St-Michel':
                                data2+=","+"yes"
                                found=True
                                break
                    if not(found):
                        data2+=","+"no"
                    found = False
                    for edu in res:
                        if 'school' in edu:
                            #'Coll\xe8ge Saint - Michel'
                            if edu["school"]["name"]=='Université libre de Bruxelles':
                                data2+=","+"yes"
                                found=True
                                break
                            """if edu["school"]["name"]=='ULB BE':
                                data2+=","+"yes"
                                found=True
                                break"""
                            if edu["school"]["name"]=='Vrije Universiteit Brussel':
                                data2+=","+"yes"
                                found=True
                                break
                            if 'ULB' in edu["school"]["name"]:
                                data2+=","+"yes"
                                found=True
                                break   
                    if not(found):
                        data2+=","+"no"
            else:
                for info in information:
                    data2+=","+"NA"
                
                for info in information2:
                    data2+=","+"NA"
                    
                #birthday
                data2+=","+"NA"
                
                # college and 
                data2+=","+"no"
                data2+=","+"no"
            
            for like in list_likes:
                data2+=","
                # if the user has not liked the page
                if not(like in [i['name'] for i in self.G.node[node]['likes'].values()]):
                    data2+=not_keyword
                data2+='liked'
                
                
            data2+=self.G.node[node].get('gender', 'unknown')
            data2+='\n'
            
            data+=data2
            print("node ", node_number + 1, " processed in " ,time.time() - start_time, "seconds")
            node_number+=1
        return attributes, data
        
    def getProfileTuples(self, file_path="C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\profiles.json"):
        #information = ['relationship_status', 'locale', 'hometown', 'education', 'languages', 'location', 'birthday']
        information = ['relationship_status', 'locale']
        tuples=[]
        
        json_data=open(file_path)
        profiles = json.load(json_data)
        json_data.close()
        
        
        for info in information:
            value_set=set()
            for person in profiles:
                value_set.add(('_'.join(profiles[person].get(info, "NA").split())))
            tuples.append((info, [x for x in value_set]))
            
        information2 = ['hometown', 'location']
        for info in information2:
            value_set=set()
            for person in profiles:
                value_set.add(('_'.join(profiles[person].get(info, {'name':"NA"})['name'].replace(',', '').split())))
            tuples.append((info, [x for x in value_set]))
        
        info='birthday'
        value_set=set()
        for person in profiles:
            test= profiles[person].get(info, "NA")
            if len(test)==3:
                value_set.add(test[2])
            else:
                value_set.add('NA')
        tuples.append((info, [x for x in value_set]))
        
        tuples.append(("College_Saint-Michel", ["yes", "no"]))
        tuples.append(("ULB", ["yes", "no"]))
            
        return tuples
        
    def get_node_attributes(self, node):
        data = ""
        data+=self.G.node[node].get('gender', 'unknown')
        return data
    
    def make_model_file(self, filename):
        data = self.get_attributes()
        
        f = open(filename + '.arff', 'w')
        f.write('@RELATION COMMUNITY\n')
        attributes=data[0]
        for attribute in attributes:
            f.write('@ATTRIBUTE '+attribute[0]+" {")
            f.write(','.join(attribute[1]))
            f.write('}\n')
        f.write('@DATA\n')
        f.write(data[1])
        f.close()
        
    def make_model_file_with_likes(self, filename, userList=""):
        data = self.get_attributes_with_likes(userList)

        f = self.getFile(filename, userList)
        f.write('@RELATION GENDER\n')
        attributes=data[0]
        for attribute in attributes:
            print(attribute[0])
            f.write('@ATTRIBUTE '+attribute[0]+" {")
            f.write(','.join(attribute[1]))
            f.write('}\n')
        f.write('@DATA\n')
        f.write(data[1])
        f.close()
    
    def make_gender_model(self, filename):
        f = open(filename + ".arff", 'w')
        f.write('@RELATION GENDER\n')
        
        attributes=self.get_gender_attributes()
        i=0
        for attribute in attributes:
            f.write('@ATTRIBUTE ')
            try:
                f.write(attribute[0])
            except UnicodeEncodeError:
                for char in attribute[0]:
                    try:
                        f.write(char)
                    except UnicodeEncodeError:
                        f.write(str(i))
            f.write(" {")
            f.write(','.join(attribute[1]))
            f.write('}\n')
            i+=1
        f.write('@DATA\n')
        f.write(self.get_gender_data())
        f.close()
        
    def make_csv_file(self):
        import pandas as pd
        
    
    def getFile(self, filename, userList):
        if userList == "":
            return open(filename + '.arff', 'w')
        else:
            return open(filename + userList[0]["name"].replace(" ", "_").replace(",", "")+ '.arff', 'w')
    
    def read_friendlists_file(self, filename):
        json_data=open(filename)
        self.friendlists = json.load(json_data)
        json_data.close()
    def generate_model_files(self, repertory="C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\"):
        self.make_model_file_with_likes(repertory+"model_file_with_likes")
        json_data=open(repertory+"friendlists.json")
        friendlists = json.load(json_data)
        json_data.close()
    
        for friendlist in friendlists:
            self.make_model_file_with_likes(repertory+"model_file_with_likes", userList=friendlist)
    
def main():
    repertory="C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\"
    graph = SocialGraph()
    graph.read_json_file(repertory + "Code\\my_network.json")
    graph.read_friendlists_file(repertory + "friendlists.json")
    graph.read_likes_file(repertory + "likes.json")
    
    # generate model files
    graph.generate_model_files()
                            
if __name__ == "__main__":
    main()