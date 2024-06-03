#Class for testing the efficacy of the algorithm

import reccomend


Class test_recs:
    
    
    def __init__(self):
    
    
    
    def pruchase(self, n, method == 'static'):
        adj_df, wardrobe = load_data()
        recs = reccomend.score_wardrobe()
        recs_list = list(recs.keys())
        if method == static:
            wardrobe += recs_list
        else:
            for i in range(n):
                wardrobe.append(recs_list[0])
                recs = reccomend.score_wardrobe(wardrobe = wardrobe)
                recs_list = list(recs.keys())
                
        return wardrobe, adj_df
                
        
        
    def complete_fits(self, outfits):
        new_wardrobe, adj_df = pruchase(10, method == 'static')
        num_fits = 0
        for outfit in adj_df.columns:
            fit = adj_df.loc[:, outfit] > 0
            fit_names = [x for x, y in zip(fit.index, fit.values) if y == True]
            is_whole = set(new_wardrobe) & set(fit_names)
            if len(is_whole) == len(fit_names):
                num_fits += 1
        
        return num_fits/len(adj_df.columns)
              
 
    
    def distributed(self):
        #Go through edges in new wardrobe graph and plot the distribution of how related all items are
        #compare this to a version where items were reccomended only by relatedness 
        #impelement a method where the user can purchase items they already have. Then count and plot the number of items                  reccomended by both similarity and measure of optimality. 
     
     
    def plot_results(self, ):
        #plot the results of the complete_fits function