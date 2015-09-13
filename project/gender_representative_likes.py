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



"""
I now must create a model file where the attribute to predict is the gender.
"""
graph.make_gender_model("../ressources/outputs/gender_model")



"""
Now it's time to produce the most representative likes:
"""

from model import Model

model = Model("../ressources/outputs/gender_model.arff")
model.GetValues()
model.TrainClassifier()
model.name_community(score='posterior')

model.max_likehood_features_for_labels()

