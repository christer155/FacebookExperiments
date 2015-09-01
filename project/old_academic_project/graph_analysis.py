import socialgraph as sg

def main():
    repertory="C:\\Users\\Heschoon\\Dropbox\\ULB\\Current trends of artificial intelligence\\Trends_project\\"
    graph = sg.SocialGraph()
    graph.read_json_file(repertory + "Code\\my_network.json")
    
    graph.read_likes_file(repertory + "likes.json")
    
    #graph.print_dendrogram()
    #graph.draw()
    #graph.draw_communities()
    #graph.draw_random_communities()
    #graph.draw_circular_communities()
    #graph.draw_spectral_communities()
    #graph.draw_shell_communities()
    
    """partition = graph.find_partition()[1]
    for community in set(partition.values()):
        print "COMMUNITY: "+str(community)
        for node in graph.G.nodes():
            if partition[node]==community:
                print graph.G.node[node].get('name', 'unknown')"""
    
    
    #graph.plot_induced_subgraphs()
    #graph.make_model_file(repertory + "model_file.arff")
    
    #graph.draw_spring_communities(full_names=True, k=500, iterations=100, scale=100.0)
        
if __name__ == "__main__":
    main()