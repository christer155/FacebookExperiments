# -*- coding: utf-8 -*-
"""
Loads saved data, convert it as a graph.
Saves the graph as JSON.
Generates a model from likes and gender.
Finds what are the best likes to predict the gender.


Created on Tue Sep  1 21:26:34 2015

@author: Heschoon
"""

import json
import networkx as nx
import graph.social_graph as gp

"""class SocialGraph:
    def __init__(self):
        self.G = nx.Graph()
        self.friendlists=None"""



repertory="../ressources/"
graph = gp.SocialGraph()
graph.read_json_file(repertory + "my_network.json")
graph.read_friendlists_file(repertory + "friendlists.json")
graph.read_likes_file(repertory + "likes.json")

"""import networkx as nx
from networkx.readwrite import json_graph


my_network = json.load(open(repertory + "my_network.json"))
friendlists = json.load(open(repertory + "friendlists.json"))
likes = json.load(open(repertory + "likes.json"))


test = json_graph.node_link_graph(my_network)"""
