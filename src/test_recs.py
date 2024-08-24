#Class for testing the efficacy of the algorithm

import reccomend as rec 


class test_recs:
    
    
    def __init__(self):
        self.rec_instance = rec.reccomend()
    
    def static_purchase(self, wardrobe, adj_df, only_new, iterations):
        recs = self.rec_instance.score_wardrobe(wardrobe, adj_df, only_new, iterations)
        recs_list = list(recs.keys()) 
        
        return recs_list
            
    def dynamic_purchase(self, wardrobe, adj_df, only_new, iterations):
        recs = self.rec_instance.score_wardrobe(wardrobe, adj_df, only_new, iterations)
        recs_list = list(recs.keys()) 
        wardrobe.append(recs_list[0])
        
        return wardrobe, recs_list
                
        
        
    def complete_fits(self, adj_df, wardrobe):
        num_fits = 0
        for outfit in adj_df.columns:
            fit = adj_df.loc[:, outfit] > 0
            fit_names = [x for x, y in zip(fit.index, fit.values) if y == True]
            is_whole = set(wardrobe) & set(fit_names)
            if len(is_whole) == len(fit_names):
                num_fits += 1
        
        return num_fits/len(adj_df.columns)
              
 
    
    def get_links(self, adj_df, wardrobe):
        graph, pieces = self.rec_instance.build_network(adj_df)
        all_edges = []
        for i, item in enumerate(wardrobe):
            
            wardrobe_copy = wardrobe[:] #creating shallow copy so that we don't change the index of the loop inside the loop. 
            piece = wardrobe_copy.pop(i)
            wardrobe_index = [pieces.index(x) for x in wardrobe_copy]
            piece_index = pieces.index(piece)
            edges = graph[piece_index, wardrobe_index] #getting all edges between the most recent addition to the wardrobe and all previous wardobe items. We can observe the distribution of all edges between new pieces and previously owned wardrobe items
            all_edges.extend(edges)
            
        return all_edges
    
    
    def num_items(self, wardrobe):
        
        '''
        Intakes the reccomended wardobe and counts the number of times an item occurs, then counts the number of times an item           has occured for every number of times an item has occured. 
        
        Parameters
        ----------
        wardobe: a list of clothing article descriptions for each wardrobe item 

        Returns
        -------
        A dictionary of how many times items have occured, and how many times items have occured these number of times across all items
        
        '''
        freq_dict = {}
        for item in wardrobe:
            if item in freq_dict.keys(): 
                freq_dict[item] += 1
            else:
                freq_dict[item] = 1
        
        freq_dict2 = {}
        for num in freq_dict.values():
            if num in freq_dict.keys():
                freq_dict2[str(num)] += 1
            else:
                freq_dict2[str(num)] = 1
 
        return freq_dict2
                
            
     
    def get_results(self, iterations, only_new = True):
        adj_df, wardrobe = self.rec_instance.load_data()
        n = len(adj_df.index) - len(wardrobe) - 1
        fits_dict = {}
        
        fits_static = [] 
        edges_static = []
        recs_list = self.static_purchase(wardrobe, adj_df, only_new, iterations)
        
        for i in range(n): #not sure why I can't just run through the whole recs_list here. Not sure why I need to calculate how many recs there are. Maybe change. 
            if recs_list[i] == 0:
                break
        
            static_wardrobe.append(recs_list[i])

           # print(len(wardrobe))
            percent_complete = self.complete_fits(adj_df, static_wardrobe)
            fits_static.append(percent_complete)
            dist_static = self.get_links(adj_df, static_wardrobe)
            edges_static.append(dist_static)
            freq_static = self.num_items(static_wardrobe)
        
            
        fits_dict['fits_static_'] = fits_static
        fits_dict['dist_static_'] = edges_static
        fits_dict['freq_static_'] = freq_static

        fits_dynamic = []
        edges_dynamic = []
        for i in range(n):
            wardrobe, recs_list = self.dynamic_purchase(wardrobe, adj_df, only_new, iterations)
            if recs_list[0] == 0:
                break
            print(recs_list)
            percent_complete = self.complete_fits(adj_df, wardrobe)
            dist_dynamic = self.get_links(adj_df, wardrobe)
            fits_dynamic.append(percent_complete) 
            edges_dynamic.append(dist_dynamic)
            freq_dynamic = self.num_items(wardrobe)
            
        fits_dict['fits_dynamic_'] = fits_dynamic
        fits_dict['dist_dynamic_'] = edges_dynamic
        fits_dict['freq_dynamic_'] = freq_dynamic
                
        return fits_dict
        
        
     
 
        
         
        
        
        
        
        