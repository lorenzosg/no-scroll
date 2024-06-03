#Class for testing the efficacy of the algorithm

import reccomend


Class test_recs:
    
    
    def __init__(self):
    
    
    
    def pruchase(self, n, method == 'static'):
        wardrobe = load_data()[1]
        recs = reccomend.score_wardrobe()
        recs_list = list(recs.keys())
        if method == static:
            wardrobe += recs_list
        else:
            for i in range(n):
                wardrobe.append(recs_list[0])
                recs = reccomend.score_wardrobe(wardrobe = wardrobe)
                recs_list = list(recs.keys())
                
        return wardrobe
                
        
        
    def complete_fits(self, outfits):
        
        
        #run through all columns of the outfits matrix and see how many of them are fully present in the aquired clothing. 
         
    
    def distributed(self):
        #Go through edges in new wardrobe graph and plot the distribution of how related all items are
        #compare this to a version where items were reccomended only by relatedness 
        #impelement a method where the user can purchase items they already have. Then count and plot the number of items                  reccomended by both similarity and measure of optimality. 
     
     
    def plot_results(self, ):
        #plot the results of the complete_fits function