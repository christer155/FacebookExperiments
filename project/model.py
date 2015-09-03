# -*- coding: utf-8 -*-
# freely inspired from 
#http://ebiquity.umbc.edu/blogger/2010/12/07/naive-bayes-classifier-in-50-lines/
#Original Author: Krishnamurthy Koduvayur Viswanathan

 
from __future__ import division
import collections
import math
import copy

"""from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts"""

"""from os import path
import sys
import wordcloud"""
 
class Model: 
        def __init__(self, arffFile):
                self.trainingFile = arffFile
                self.features = {}      #all feature names and their possible values (including the class label)
                self.featureNameList = []       #this is to maintain the order of features as in the arff
                self.featureCounts = collections.defaultdict(lambda: 1)#contains tuples of the form (label, feature_name, feature_value)
                self.featureVectors = []        #contains all the values and the label as the last entry
                self.labelCounts = collections.defaultdict(lambda: 0)   #these will be smoothed later
                self.membersCounts=collections.defaultdict(lambda: 0)
 
        def TrainClassifier(self):
                for fv in self.featureVectors:
                        self.labelCounts[fv[len(fv)-1]] += 1 #udpate count of the label
                        for counter in range(0, len(fv)-1):
                                self.featureCounts[(fv[len(fv)-1], self.featureNameList[counter], fv[counter])] += 1
                
                self.membersCounts=copy.deepcopy(self.labelCounts)
 
                for label in self.labelCounts:  #increase label counts (smoothing). remember that the last feature is actually the label
                        for feature in self.featureNameList[:len(self.featureNameList)-1]:
                                self.labelCounts[label] += len(self.features[feature])
 
        def Classify(self, featureVector):      #featureVector is a simple list like the ones that we use to train
                probabilityPerLabel = {}
                for label in self.labelCounts:
                        logProb = 0
                        for featureValue in featureVector:
                                logProb += math.log(self.featureCounts[(label, self.featureNameList[featureVector.index(featureValue)], featureValue)]/self.labelCounts[label])
                        probabilityPerLabel[label] = (self.labelCounts[label]/sum(self.labelCounts.values())) * math.exp(logProb)
                #print(probabilityPerLabel
                return max(probabilityPerLabel, key = lambda classLabel: probabilityPerLabel[classLabel])
                                
        def GetValues(self):
                file = open(self.trainingFile, 'r')
                for line in file:
                        if line[0] != '@':  #start of actual data
                                self.featureVectors.append([x.strip() for x in line.strip().split(',')])
                        else:   #feature definitions
                                if line.strip().lower().find('@data') == -1 and (not line.lower().startswith('@relation')):
                                        self.featureNameList.append(line.strip().split()[1])
                                        self.features[self.featureNameList[len(self.featureNameList) - 1]] = [featureName.strip() for featureName in line[line.find('{')+1: line.find('}')].strip().split(',')]
                file.close()
                
 
        def TestClassifier(self, arffFile):
                file = open(arffFile, 'r')
                for line in file:
                        if line[0] != '@':
                                vector = [x.strip() for x in line.strip().split(',')]
                                print("classifier: " + self.Classify(vector) + " given " + vector[len(vector) - 1])
        
        def PerformanceClassifier(self, arffFile):
                file = open(arffFile, 'r')
                results=[0,0]
                for line in file:
                        if line[0] != '@':
                                vector = [x.strip() for x in line.strip().split(',')]
                                max_likelihood = self.Classify(vector)
                                results[0]+= (max_likelihood ==vector[len(vector) - 1])
                                results[1]+=1
                                print("classifier: " + self.Classify(vector) + " given " + vector[len(vector) - 1])
                print("The classifier is "+str(results[0]/results[1])+" percent accurate.")    
        
        def test_max_lik(self):
            for label in self.features[self.featureNameList[-1]]:
                max_lik=[]
                for feature in self.featureNameList[:-1]:
                    for value in self.features[feature]:
                        lk = self.posterior(label, feature, value)
                        max_lik.append((lk, feature, value))
                print("Label: "+str(label))
                max_lik=sorted(max_lik, key=lambda tup: tup[0], reverse=True)#
                
                max_lik=[element for element in max_lik if not(element[2].startswith('not_'))]
                
                self.print_list(max_lik, 10)
                
        def likelihood(self, label, feature, value):
            # likelihood of feature given the class
            return float(self.featureCounts[(label, feature, value)])/float(self.labelCounts[label])
            
        def print_list(self, feature_list, number):
            print("Rank".center(4), "Score".rjust(15), "Feature".center(50), "Value".ljust(0))
            for i in range(min(number, len(feature_list))):
                print(str(i+1).rjust(4), "{0:.2f}".format(feature_list[i][0]).rjust(15)),#str(feature_list[i][0])
                # Note trailing comma on previous line
                print(feature_list[i][1].center(50), feature_list[i][2].ljust(0))

                
        def compute_max_likelihood_value(self, feature, label):
            mlv=(0.0,"")
            for value in self.features[feature]:
                if self.feature_label_likelihood(value, label) > mlv:
                    mlv=(self.feature_label_likelihood(value, label), value)
            return mlv
        
        def compute_max_posterior_value(self, feature, label):
            mlv=(0.0,"")
            for value in self.features[feature]:
                if self.feature_label_likelihood(value, label) > mlv:
                    mlv=(self.feature_label_likelihood(value, label), value)
            return mlv
        
        def posterior(self, label, feature, value):
            # conditional probabilty
            post = self.featureCounts[(label, feature, value)]/self.labelCounts[label]
            # class probability
            post = post* self.labelCounts[label]/sum(self.labelCounts.values())
            
            # feature probability
            feature_probability=0.0
            
            for label2 in self.labelCounts:
                feature_probability+=self.featureCounts[(label2, feature, value)]
            feature_probability=feature_probability/sum(self.labelCounts.values())
            
            post = post /feature_probability
            return post
            
                       
        def name_community(self, score='likehood', filter_words=True):
            for label in self.features[self.featureNameList[-1]]:
                if label !="other":
                    max_lik=[]
                    for feature in self.featureNameList[:-1]:
                        for value in self.features[feature]:
                            lk=None
                            if score == 'likehood':
                                lk = self.likelihood(label, feature, value)
                            elif score == 'posterior':
                                lk = self.posterior(label, feature, value)
                            else:
                                print('unknown score tag') 
                            max_lik.append((lk, feature, value))
                    print("Community: "+str(label))
                    print('Number of members:', self.membersCounts[label])
                    max_lik=sorted(max_lik, key=lambda tup: tup[0], reverse=True)#
                    
                    if filter_words:
                        max_lik=[element for element in max_lik if not(element[2].startswith('not_'))]
                    
                    #self.print_list(max_lik, 15)
                    if label == '3':
                        for element in max_lik[0:15]:
                            if element[1]=='locale':
                                continue 
                            if element[1]=='gender' or element[1]=='birthday' or element[1]=='location' or element[1]=='hometown':
                                print((element[2].replace('_', ' ').replace('é', 'e')+' ')*(int(element[0]*100)))
                            else:
                                print((element[1].replace('_', ' ').replace('é', 'e')+' ')*(int(element[0]*100)))
                    
                    
		
if __name__ == "__main__":
        repertory="C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\"
        #model = Model(repertory+"Code\\tennis.txt")
        #model = Model(repertory+"model_file.arff")
        """model = Model(repertory+"model_file_with_likes.arff")
        model.GetValues()
        model.TrainClassifier()"""
        #model.TestClassifier(repertory+"Code\\tennis.txt")
        #model.PerformanceClassifier(repertory+"model_file.arff")
        #model.PerformanceClassifier(repertory+"model_file_with_likes.arff")
        #model.test_max_lik() DEPRECATED
        
        
        #model.name_community()
        
        #test on Louvain's algorihtms communities
        print('#############################')
        print("LOUVAIN COMMUNITIES")
        print('#############################')
        model = Model(repertory+"model_file_with_likes.arff")
        model.GetValues()
        model.TrainClassifier()
        model.name_community(score='posterior')
        
        #test on the categories from user friendlists
        """import json
        json_data=open("C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\friendlists.json")
        friendlists = json.load(json_data)
        json_data.close()
    
        print('#############################'
        print('USER AND FACEBOOK FRIENDLISTS'
        print('#############################'
        for friendlist in friendlists:
            if friendlist[1]:
                print('FRIENDLIST'
                print('Type:', friendlist[0]["list_type"]
                model = Model(repertory+"model_file_with_likes"+friendlist[0]["name"].encode('ascii', 'ignore').replace(" ", "_").replace(",", "") +".arff")
                model.GetValues()
                model.TrainClassifier()
                model.name_community(score='posterior')"""
                
                
        #make cloudwords
        """
        Rank           Score                      Feature                       Value
   1            0.39                 Impro-Vocation_Ulb                 liked
   2            0.33                        ULB                         yes
   3            0.32                      Les_PANS                      liked
   4            0.29                    Typique_ULB                     liked
   5            0.27                       gender                       female
   6            0.27                       locale                       fr_FR
   7            0.27                      birthday                      1989
   8            0.27                      location                      Brussels_Belgium
   9            0.26                College_Saint-Michel                no
  10            0.26 FBIA_-_Fédération_Belge_d'Improvisation_Amateur  liked
  11            0.26                      hometown                      Brussels_Belgium
  12            0.26                    BuzzFil.com                     liked
  13            0.25               Cercle_Impro-vocation                liked
  14            0.25                    Cercle_OPAC                     liked
  15            0.24                     Tout-Teddy                     liked
Community: 2
Number of members: 33
Rank           Score                      Feature                       Value
   1            0.33               Cercle_Impro-vocation                liked
   2            0.32                 Impro-Vocation_Ulb                 liked
   3            0.27               Les_Oubliés_du_Mardi                liked
   4            0.26                   Phobia_Presse                    liked
   5            0.21                        ULB                         yes
   6            0.19                       gender                       female
   7            0.19                      birthday                      1993
   8            0.18              Les_Inconnus_-_Officiel               liked
   9            0.18                      location                      Etterbeek
  10            0.18              Campus_en_Transition_ULB              liked
  11            0.18                    Chips_et_Noi                    liked
  12            0.18            Coiffures_simples_à_faire.             liked
  13            0.18    Game_of_Thrones_(Le_Trône_de_Fer)_-_France     liked
  14            0.18                    SMBC_Comics                     liked
  15            0.18                College_Saint-Michel                no

        """
        cercle2 = ["Cercle Impro-vocation", "Impro-Vocation Ulb", "Les Oubliés du Mardi", "Phobia Presse", "ULB", "female",
        "1993", """Les Inconnus - Officiel""", "Etterbeek", 
        "Campus en Transition ULB", "Chips et Noi", "Coiffures simples à faire", "Game of Thrones", "SMBC Comics"]
        cercle2_scores =[
                    0.33,
                    0.32,
                    0.27,
                    0.26,
                    0.21,
                    0.19,
                    0.19,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18,
                    0.18
                ]
        cercle1 = ["Impro-Vocation", "ULB", "Les PANS", "Typique ULB", "female", "1989",
        "Brussels", """FBIA_-_Fédération_Belge_d'Improvisation_Amateur""", "Belgium", 
        "BuzzFil.com", "Cercle Impro-vocation", "Cercle OPAC", "Tout-Teddy"]
        cercle1_scores = [
                    0.39,
                    0.33,
                    0.32,
                    0.29,
                    0.27,
                    0.27,
                    0.27,
                    0.26,
                    0.26,
                    0.25,
                    0.25,
                    0.24]
                    
        cercle1Tuples=[]
        cercle2Tuples=[]
        for element in cercle1:
            for count in cercle1_scores:
                cercle1Tuples.append((element, count))
        for element in cercle2:
            for count in cercle2_scores:
                cercle2Tuples.append((element, count))
        """for element in cercle1Tuples:
            print((element[0]+' ')*int(element[1]*50.0)"""
            
        """for element in cercle1:
            print(element"""
        
        """max_word_size = 80
        width=400
        height=400
        layout = 3
        background_color = (255, 255, 255)
        
        tags = make_tags(cercle1Tuples, maxsize=max_word_size)
        
        create_tag_image(tags, 'cloud_large.png', size=(width, height), layout=layout, fontname='Lobster', background = background_color)"""
        