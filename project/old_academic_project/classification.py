import socialgraph as sg
import Model

def main():
    model_file = ""
    model_file2 = "C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\model_file_with_likes.arff"
    my_network = "C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\Code\\my_network.json"
    graph = sg.SocialGraph()
    graph.read_json_file(my_network)
    
    # produce model file
    #produce for each community?
    # no, reuse ifnormation from Model! Create heritancy!
    
    #model = Model(model_file)
    model = Model(model_file2)
    model.GetValues()
    model.TrainClassifier()
    
        
if __name__ == "__main__":
    main()