#Class for testing the efficacy of the algorithm

import reccomend as rec 


class test_recs:
    
    
    def __init__(self):
    
    
    def purchase(self, n, wardrobe = 'wardrobe', method == 'static', optimal = True):
        recs = rec.score_wardrobe(optimal = optimal)
        recs_list = [x for x, y in zip(recs.keys(), recs.values) if y > 0]
        if method == static:
            wardrobe += recs_list[:n]
            
        else:
            recs = rec.score_wardrobe(wardrobe = wardrobe)
            recs_list = [x for x, y in zip(recs.keys(), recs.values) if y > 0]
            wardrobe.append(recs_list[0])
                
        return wardrobe, recs_list
                
        
    
    
    
    def purchase2(self, n, optimal = True):
        adj_df, wardrobe = rec.load_data()
        recs = rec.score_wardrobe(optimal = optimal)
        recs_list = [x for x, y in zip(recs.keys(), recs.values) if y > 0]
        if method == static:
            wardrobe += recs_list[:n]
            
        else:
            for i in range(n):
                if list(recs.values()) == 0:
                    break 
                wardrobe.append(recs_list[0])
                recs = rec.score_wardrobe(wardrobe = wardrobe)
                recs_list = list(recs.keys())
                
        return wardrobe, recs
                
        
        
    def complete_fits(self, adj_df = 'adj_df', wardrobe = 'wardrobe'):
        num_fits = 0
        for outfit in adj_df.columns:
            fit = adj_df.loc[:, outfit] > 0
            fit_names = [x for x, y in zip(fit.index, fit.values) if y == True]
            is_whole = set(wardrobe) & set(fit_names)
            if len(is_whole) == len(fit_names):
                num_fits += 1
        
        return num_fits/len(adj_df.columns)
              
 
    
    def distributed(self, network = 'adj_df', wardrobe = 'wardrobe'):
        all_edges = []
        for item in wardrobe:
            wardrobe_copy = wardrobe[:]
            piece = wardrobe_copy.pop(item)
            edges = network[piece, wardrobe]
            all_edges += edges
            
        return all_edges
    
    
    def num_items():
        freq_dict = {}
        for item in wardrobe:
            if item in freq_dict: 
                freq_dict[item] += 1
            else:
                freq_dict = 1
        
        freq_dict2 = {}
            for num in freq_dict2.values():
                if num in freq_dict2:
                    freq_dict2[num] += 1
                else:
                    freq_dict2[num] = 1
        
        return freq_dict2
                
            
        
        
        
        #Go through edges in new wardrobe graph and plot the distribution of how related all items are
        #compare this to a version where items were reccomended only by relatedness 
        #implement a method where the user can purchase items they already have. Then count and plot the number of items                  reccomended by both similarity and measure of optimality. 
     
     
    def get_results(self, optimal = 'optimal'):
        adj_df, wardrobe = rec.load_data()
        n = len(adj_df.columns) - len(wardrobe)
        fits_dict = {}
        
        fits_static = [] 
        edges_static = []
        for i in range(n):
            wardrobe, recs_list = purchase(n, wardrobe, optimal, method == 'static')
            if recs_list[i] == 0:
                break
            percent_complete = complete_fits(adj_df, wardrobe)
            dist_static = distributed(adj_df, wardrobe)
            fits_static.append(percent_complete)
            edges_static.append(dist_static)
            freq_static = num_items(wardrobe)
            
        fits_dict['fits_static_' + str(i)] = fits_static
        fits_dict['dist_static_' + str(i)] = edges_static
        fits_dict['freq_static_' + str(i)] = freq_static

        fits_dynamic = []
        edges_dynamic = []
        for i in range(n):
            wardrobe, recs_list = purchase(n, wardrobe, optimal, method == 'dyanmic')
            if recs_list[0] == 0:
                break
            percent_complete = complete_fits(adj_df, wardrobe)
            dist_dynamic = distributed(adj_df, wardrobe)
            fits_dynamic.append(percent_complete) 
            edges_dynamic.append(dist_dynamic)
            freq_dynamic = num_items(wardrobe)
            
        fits_dict['fits_dynamic_' + str(i)] = fits_dynamic
        fits_dict['dist_dynamic_' + str(i)] = edges_dynamic
        fits_dict['freq_dynamic_' + str(i)] = freq_dynamic
                
        return fits_dict
        
        
     
                
                
        #I want to go through and simulate purchases for n+1 till there are no further reccomendations. 
        
        
        
        
        
        