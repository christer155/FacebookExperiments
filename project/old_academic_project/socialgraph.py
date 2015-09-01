# -*- coding: utf-8 -*-
import community
import networkx as nx
import matplotlib.pyplot as plt
import json
from networkx.readwrite import json_graph
from sets import Set
from pprint import pprint
import collections

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
        
    def find_partition(self):
        g= self.G
        partition = community.best_partition(g)
        nx.set_node_attributes(g, 'partition', partition)
        return g, partition
        
    def draw(self):
        nx.draw(self.G)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_draw.pdf")
        
    def get_colors(self):
        return ['red', 'blue', 'green', 'cyan', 'magenta', 'yellow']
    
    def draw_communities(self):
        partition = self.find_partition()[1]
        
        #we rassemble lonely nodes under the same category
        counts = collections.defaultdict(lambda: 0)
        for node in partition:
            counts[partition[node]]+=1
        min_bad = 1000
        for node in partition:
            if counts[partition[node]]<3:
                if partition[node]<min_bad:
                    min_bad=partition[node]
        for node in partition:
            if partition[node]>min_bad:
                partition[node]=min_bad
                
        for community in counts:
            print 'Community:', community, ': ', counts[community]
        
        node_color=[float(partition[v]) for v in partition]
        
        # normalize the colors
        maximum = max(node_color)
        if maximum!=0.0:
            node_color=[x/maximum for x in node_color]

        labels = self.compute_labels()
        nx.draw(self.G,node_color=node_color, labels=labels, cmap=plt.cm.hsv)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_communities.pdf")
        
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
        
    def draw_circular(self):
        #first compute the best partition
        partition = community.best_partition(self.G)
        #drawing
        size = float(len(set(partition.values())))
        pos = nx.spring_layout(self.G)
        count = 0.
        for com in set(partition.values()) :
            count = count + 1.
            list_nodes = [nodes for nodes in partition.keys()
                                if partition[nodes] == com]
        nx.draw_networkx_nodes(self.G, pos, list_nodes, node_size = 20,
                                node_color = str(count / size))
        nx.draw_networkx_edges(self.G,pos, alpha=0.5)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_circular2.pdf")
        
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
        self.G = json_graph.load(open(filename))
        print "Read in file ", filename
        
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
        
    def print_dendrogram(self):
        dendo = community.generate_dendogram(self.G)
        for level in range(len(dendo) - 1) :
            print "partition at level", level, "is", community.partition_at_level(dendo, level)
    
    # create the attribute vector of dictionary
    def get_attributes(self):
        # create the list of attributes
        partition = self.find_partition()[1]
        attributes = []
        attributes.append(('gender', ['male', 'female', 'unknown']))
        attributes.append(('community', [str(res) for res in list(Set([partition[v] for v in partition]))]))
        
        # create the content of each nodes line
        data = ""
        for node in self.G.nodes():
            data+=self.get_node_attributes(node)+','+str(partition[node])+'\n'
        return attributes, data
        
    # create the attribute vector of dictionary
    def get_attributes_with_likes(self, userList):
        not_keyword= 'not_'
        list_likes={}
        for node in self.G.nodes():
            for like in self.G.node[node]['likes']:
                list_likes[like]=self.G.node[node]['likes'][like]
        set_ = Set(list_likes.keys())
        set_ = Set([i['name'] for i in list_likes.values()])
        list_likes=sorted(set_)
        
        # create the list of attributes
        attributes = []
        attributes.append(('gender', ['male', 'female', 'unknown']))
        
        # add other profile informations
        attributes.extend(self.getProfileTuples())
        
        partition = self.find_partition()[1]
        for like in list_likes:
                attributes.append(('_'.join(like.encode('utf-8').split()), ['liked', not_keyword+'liked']))
        if userList=="":
            attributes.append(('community', [str(res) for res in list(Set([partition[v] for v in partition]))]))
        else:
            attributes.append((userList[0]["name"].encode('ascii', 'ignore').replace(" ", "_").replace(",", ""), ["other", userList[0]["name"].encode('ascii', 'ignore').replace(" ", "_").replace(",", "")]))
            
        json_data=open("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\profiles.json")
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
            data2=self.get_node_attributes(node)
            
            #add other profile informations
            
            if node in profiles:
                
                for info in information:
                    data2+=","+('_'.join(profiles[node].get(info, "not_found").split()))
                
                for info in information2:
                    data2+=","+('_'.join(profiles[node].get(info, {'name':unicode("not_found")})['name'].encode('ascii', 'ignore').replace(',', '').split()))
                 
                info = 'birthday'
                test =profiles[node].get(info, "0/0/not_found").split('/')
                if len(test)==3:
                    data2+=","+test[2]
                else:
                    data2+=","+'not_found'   
                    
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
                            if edu["school"]["name"].encode('utf8')=='Collège Saint - Michel':
                                data2+=","+"yes"
                                found=True
                                break
                            if edu["school"]["name"].encode('utf8')=='Collège St-Michel':
                                data2+=","+"yes"
                                found=True
                                break
                    if not(found):
                        data2+=","+"no"
                    found = False
                    for edu in res:
                        if 'school' in edu:
                            #'Coll\xe8ge Saint - Michel'
                            if edu["school"]["name"].encode('utf8')=='Université libre de Bruxelles':
                                data2+=","+"yes"
                                found=True
                                break
                            """if edu["school"]["name"].encode('utf8')=='ULB BE':
                                data2+=","+"yes"
                                found=True
                                break"""
                            if edu["school"]["name"].encode('utf8')=='Vrije Universiteit Brussel':
                                data2+=","+"yes"
                                found=True
                                break
                            if 'ULB' in edu["school"]["name"].encode('utf8'):
                                data2+=","+"yes"
                                found=True
                                break   
                    if not(found):
                        data2+=","+"no"
            else:
                for info in information:
                    data2+=","+"not_found"
                
                for info in information2:
                    data2+=","+"not_found"
                    
                #birthday
                data2+=","+"not_found"
                
                # college and 
                data2+=","+"no"
                data2+=","+"no"
            
            for like in list_likes:
                data2+=","
                # if the user has not liked the page
                if not(like in [i['name'] for i in self.G.node[node]['likes'].values()]):
                    data2+=not_keyword
                data2+='liked'
                
            if userList=="":
                data2+=','+str(partition[node])+'\n'
            else:
                #
                if node in userList[1]:
                    data2+=","+userList[0]["name"].encode('ascii', 'ignore').replace(" ", "_").replace(",", "")+'\n'
                else:
                    data2+=","+"other"+'\n'
            
            
            data+=data2
            print node_number , " processed in " ,time.time() - start_time, "seconds"
            node_number+=1
        return attributes, data
        
    def getProfileTuples(self):
        #information = ['relationship_status', 'locale', 'hometown', 'education', 'languages', 'location', 'birthday']
        information = ['relationship_status', 'locale']
        tuples=[]
        
        json_data=open("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\profiles.json")
        profiles = json.load(json_data)
        json_data.close()
        
        
        for info in information:
            value_set=Set()
            for person in profiles:
                value_set.add(('_'.join(profiles[person].get(info, "not_found").split())))
            tuples.append((info, [x for x in value_set]))
            
        information2 = ['hometown', 'location']
        for info in information2:
            value_set=Set()
            for person in profiles:
                value_set.add(('_'.join(profiles[person].get(info, {'name':"not_found"})['name'].encode('ascii', 'ignore').replace(',', '').split())))
            tuples.append((info, [x for x in value_set]))
        
        info='birthday'
        value_set=Set()
        for person in profiles:
            test= profiles[person].get(info, "0/0/not_found").split('/')
            if len(test)==3:
                value_set.add(test[2])
            else:
                value_set.add('not_found')
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
        f.write('@RELATION COMMUNITY\n')
        attributes=data[0]
        for attribute in attributes:
            f.write('@ATTRIBUTE '+attribute[0]+" {")
            f.write(','.join(attribute[1]))
            f.write('}\n')
        f.write('@DATA\n')
        f.write(data[1])
        f.close()
    
    def getFile(self, filename, userList):
        if userList == "":
            return open(filename + '.arff', 'w')
        else:
            return open(filename + userList[0]["name"].encode('ascii', 'ignore').replace(" ", "_").replace(",", "")+ '.arff', 'w')
    
    def plot_induced_subgraphs(self):
        plt.figure(1)
        partition = self.find_partition()[1]
        communities = [partition[v] for v in partition]
        newGraph=self.G
        for community in communities:
            nx.subgraph(newGraph, [key for key in partition if partition[key]==community])
        node_color=[float(partition[v]) for v in partition]
        labels =  {}
        for node in newGraph.nodes():
            labels[node]= newGraph.node[node].get('name', '')
        nx.draw_spring(newGraph,node_color=node_color, labels=labels)
        plt.show()
        plt.savefig("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\graphs\\graph_induced.pdf")
        
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
        
    # display the social graph
    #graph.draw_communities()
    
    #display of a simple graph
    """graph = SocialGraph()
    graph.generate_test_graph()
    
    
    graph.save_to_jsonfile("saved_graph")
    graph.G = nx.Graph()
    graph.read_json_file("saved_graph")
    graph.add_friends([{u'name': u'', u'id': u'100008030703218'}])
    graph.add_friends([{u'name': u'H', u'id': u'739115516'}])
    graph.add_friendships({'100008030703218':[{u'name': u'', u'id': u'739115516'}]})
    
    #graph.make_model_file("model_file.arff")
    
    graph.print_dendrogram()
    
    #graph.plot_induced_subgraphs()
    
    graph.draw_communities()
    #graph.draw_circular()
    
    #display of the partitions
    partition = graph.find_partition()[1]
    for community in set(partition.values()):
        print "COMMUNITY: "+str(community)
        for node in graph.G.nodes():
            if partition[node]==community:
                print graph.G.node[node].get('name', 'unknown')"""
            
                            
if __name__ == "__main__":
    main()